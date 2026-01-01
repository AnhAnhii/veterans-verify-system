"""
Veterans Verification CLI
Command-line interface for verifying veteran status

Usage:
    veterans-cli verify --name "John Doe" --birth 1985-03-15 --branch Army
    veterans-cli lookup --name "John Doe"
    veterans-cli history
    veterans-cli status <verification_id>
"""

import click
import json
import os
from pathlib import Path
from datetime import date

from .api_client import APIClient
from .config import Config, get_config, save_config


# Rich console for pretty output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

if RICH_AVAILABLE:
    console = Console()
else:
    console = None


def print_success(msg):
    if console:
        console.print(f"[green]✓[/green] {msg}")
    else:
        print(f"✓ {msg}")


def print_error(msg):
    if console:
        console.print(f"[red]✗[/red] {msg}")
    else:
        print(f"✗ {msg}")


def print_info(msg):
    if console:
        console.print(f"[blue]ℹ[/blue] {msg}")
    else:
        print(f"ℹ {msg}")


@click.group()
@click.version_option(version="1.0.0", prog_name="veterans-cli")
def cli():
    """Veterans Verification CLI - Verify military veteran status"""
    pass


@cli.command()
@click.option("--api-key", required=True, help="Your API key")
@click.option("--api-url", default="http://localhost:8000", help="API base URL")
def configure(api_key: str, api_url: str):
    """Configure CLI with API credentials"""
    config = Config(api_key=api_key, api_url=api_url)
    save_config(config)
    print_success(f"Configuration saved successfully!")
    print_info(f"API URL: {api_url}")


@cli.command()
@click.option("--first-name", "-fn", required=True, help="First name")
@click.option("--last-name", "-ln", required=True, help="Last name")
@click.option("--birth", "-b", required=True, help="Birth date (YYYY-MM-DD)")
@click.option("--branch", "-br", required=True, 
              type=click.Choice([
                  "Army", "Navy", "Air Force", "Marine Corps", "Coast Guard",
                  "Space Force", "Army National Guard", "Army Reserve",
                  "Air National Guard", "Air Force Reserve", "Navy Reserve",
                  "Marine Corps Reserve", "Coast Guard Reserve"
              ]),
              help="Military branch")
@click.option("--status", "-s", default="VETERAN",
              type=click.Choice(["VETERAN", "ACTIVE_DUTY", "RESERVE", "RETIRED"]),
              help="Military status")
@click.option("--discharge", "-d", help="Discharge date (YYYY-MM-DD)")
@click.option("--email", "-e", required=True, help="Email address")
@click.option("--service", default="chatgpt",
              type=click.Choice(["chatgpt", "spotify", "youtube", "google_one"]),
              help="Service to verify for")
def verify(first_name: str, last_name: str, birth: str, branch: str, 
           status: str, discharge: str, email: str, service: str):
    """Submit a new verification request"""
    config = get_config()
    if not config:
        print_error("Not configured. Run 'veterans-cli configure' first.")
        return
    
    client = APIClient(config.api_url, config.api_key)
    
    print_info(f"Creating verification for {service}...")
    
    try:
        # Create verification
        create_result = client.create_verification(service)
        
        if not create_result.get("verificationId"):
            print_error("Failed to create verification")
            return
        
        verification_id = create_result["verificationId"]
        print_success(f"Verification created: {verification_id}")
        
        # Submit veteran info
        print_info("Submitting veteran information...")
        
        submit_result = client.submit_verification(
            verification_id=verification_id,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth,
            branch=branch,
            military_status=status,
            discharge_date=discharge,
            email=email
        )
        
        result_status = submit_result.get("status", "unknown")
        message = submit_result.get("message", "")
        
        if result_status == "approved":
            print_success(f"🎉 Verification APPROVED! {message}")
        elif result_status == "document_required":
            print_info(f"📄 Document upload required. {message}")
            print_info(f"Upload at: https://yoursite.com/verify/{verification_id}/upload")
        elif result_status == "processing":
            print_info(f"⏳ Verification processing. {message}")
        else:
            print_error(f"Verification failed: {message}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")


@cli.command()
@click.option("--first-name", "-fn", help="First name to search")
@click.option("--last-name", "-ln", help="Last name to search")
@click.option("--source", "-s", default="all",
              type=click.Choice(["all", "grave", "vlm", "army"]),
              help="Data source to search")
def lookup(first_name: str, last_name: str, source: str):
    """Search VA databases for veteran records"""
    if not first_name and not last_name:
        print_error("At least first name or last name is required")
        return
    
    config = get_config()
    if not config:
        print_error("Not configured. Run 'veterans-cli configure' first.")
        return
    
    client = APIClient(config.api_url, config.api_key)
    
    print_info(f"Searching VA records for: {first_name or ''} {last_name or ''}...")
    
    try:
        if source == "all":
            results = client.search_all_sources(first_name, last_name)
        elif source == "grave":
            results = client.search_grave_locator(first_name, last_name)
        elif source == "vlm":
            results = client.search_vlm(first_name, last_name)
        elif source == "army":
            results = client.search_army_explorer(first_name, last_name)
        
        if RICH_AVAILABLE:
            display_results_rich(results, source)
        else:
            display_results_plain(results, source)
            
    except Exception as e:
        print_error(f"Error: {str(e)}")


def display_results_rich(results, source):
    """Display results using Rich tables"""
    if source == "all":
        total = results.get("totalResults", 0)
        console.print(f"\n[bold]Found {total} results across all sources[/bold]\n")
        
        for source_name, source_data in results.get("sources", {}).items():
            if source_data.get("results"):
                table = Table(title=f"{source_name.upper()} Results")
                table.add_column("Name", style="cyan")
                table.add_column("Branch", style="green")
                table.add_column("Rank")
                table.add_column("Cemetery")
                table.add_column("Dates")
                
                for r in source_data["results"]:
                    table.add_row(
                        r.get("name", "-"),
                        r.get("branch", "-"),
                        r.get("rank", "-"),
                        r.get("cemetery", "-"),
                        r.get("serviceDates", "-")
                    )
                
                console.print(table)
                console.print()
    else:
        records = results.get("results", [])
        console.print(f"\n[bold]Found {len(records)} results[/bold]\n")
        
        if records:
            table = Table()
            table.add_column("Name", style="cyan")
            table.add_column("Branch", style="green")
            table.add_column("Rank")
            table.add_column("Cemetery")
            table.add_column("Dates")
            
            for r in records:
                table.add_row(
                    r.get("name", "-"),
                    r.get("branch", "-"),
                    r.get("rank", "-"),
                    r.get("cemetery", "-"),
                    r.get("serviceDates", "-")
                )
            
            console.print(table)


def display_results_plain(results, source):
    """Display results in plain text"""
    if source == "all":
        total = results.get("totalResults", 0)
        print(f"\nFound {total} results across all sources\n")
        
        for source_name, source_data in results.get("sources", {}).items():
            if source_data.get("results"):
                print(f"\n=== {source_name.upper()} ===")
                for r in source_data["results"]:
                    print(f"  Name: {r.get('name', '-')}")
                    print(f"  Branch: {r.get('branch', '-')}")
                    print(f"  Rank: {r.get('rank', '-')}")
                    print(f"  Cemetery: {r.get('cemetery', '-')}")
                    print()
    else:
        records = results.get("results", [])
        print(f"\nFound {len(records)} results\n")
        for r in records:
            print(f"  Name: {r.get('name', '-')}")
            print(f"  Branch: {r.get('branch', '-')}")
            print(f"  Rank: {r.get('rank', '-')}")
            print(f"  Cemetery: {r.get('cemetery', '-')}")
            print()


@cli.command()
@click.option("--page", "-p", default=1, help="Page number")
@click.option("--limit", "-l", default=10, help="Results per page")
def history(page: int, limit: int):
    """View verification history"""
    config = get_config()
    if not config:
        print_error("Not configured. Run 'veterans-cli configure' first.")
        return
    
    client = APIClient(config.api_url, config.api_key)
    
    try:
        results = client.get_history(page, limit)
        
        if RICH_AVAILABLE:
            table = Table(title="Verification History")
            table.add_column("ID", style="dim")
            table.add_column("Service", style="cyan")
            table.add_column("Veteran")
            table.add_column("Status", style="bold")
            table.add_column("Created")
            
            for item in results.get("items", []):
                status_style = {
                    "approved": "green",
                    "rejected": "red",
                    "pending": "yellow",
                    "processing": "blue",
                    "document_required": "orange"
                }.get(item.get("status", ""), "")
                
                table.add_row(
                    item.get("id", "-")[:8] + "...",
                    item.get("serviceType", "-"),
                    item.get("veteranName", "-"),
                    f"[{status_style}]{item.get('status', '-')}[/{status_style}]",
                    item.get("createdAt", "-")[:10]
                )
            
            console.print(table)
            console.print(f"\nPage {page} of {(results.get('total', 0) // limit) + 1}")
        else:
            print("\n=== Verification History ===")
            for item in results.get("items", []):
                print(f"ID: {item.get('id', '-')[:8]}...")
                print(f"Service: {item.get('serviceType', '-')}")
                print(f"Status: {item.get('status', '-')}")
                print(f"Created: {item.get('createdAt', '-')[:10]}")
                print()
                
    except Exception as e:
        print_error(f"Error: {str(e)}")


@cli.command()
@click.argument("verification_id")
def status(verification_id: str):
    """Check status of a verification"""
    config = get_config()
    if not config:
        print_error("Not configured. Run 'veterans-cli configure' first.")
        return
    
    client = APIClient(config.api_url, config.api_key)
    
    try:
        result = client.get_status(verification_id)
        
        status_value = result.get("status", "unknown")
        
        if RICH_AVAILABLE:
            status_color = {
                "approved": "green",
                "rejected": "red",
                "pending": "yellow",
                "processing": "blue",
                "document_required": "orange3"
            }.get(status_value, "white")
            
            console.print(Panel(
                f"[bold]Verification ID:[/bold] {verification_id}\n"
                f"[bold]Status:[/bold] [{status_color}]{status_value.upper()}[/{status_color}]\n"
                f"[bold]Service:[/bold] {result.get('serviceType', '-')}\n"
                f"[bold]Created:[/bold] {result.get('createdAt', '-')[:19]}",
                title="Verification Status"
            ))
        else:
            print(f"\n=== Verification Status ===")
            print(f"ID: {verification_id}")
            print(f"Status: {status_value.upper()}")
            print(f"Service: {result.get('serviceType', '-')}")
            print(f"Created: {result.get('createdAt', '-')[:19]}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")


def main():
    cli()


if __name__ == "__main__":
    main()
