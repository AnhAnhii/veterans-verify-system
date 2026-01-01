-- Veterans Verification System - Initial Schema
-- Run this in Supabase SQL Editor

-- ============================================
-- 1. PROFILES TABLE (extends Supabase Auth)
-- ============================================
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    organization TEXT,
    api_key TEXT UNIQUE DEFAULT gen_random_uuid()::TEXT,
    role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Auto-create profile on user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, email, full_name)
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', '')
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for auto-creating profile
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- ============================================
-- 2. MILITARY BRANCHES REFERENCE TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS public.military_branches (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    sheerid_org_id INTEGER,
    is_active BOOLEAN DEFAULT true
);

-- Insert military branches
INSERT INTO public.military_branches (code, name, sheerid_org_id) VALUES
    ('ARMY', 'Army', 4070),
    ('NAVY', 'Navy', 4072),
    ('AIR_FORCE', 'Air Force', 4073),
    ('MARINE_CORPS', 'Marine Corps', 4071),
    ('COAST_GUARD', 'Coast Guard', 4074),
    ('SPACE_FORCE', 'Space Force', 4544268),
    ('ARMY_NATIONAL_GUARD', 'Army National Guard', 4075),
    ('ARMY_RESERVE', 'Army Reserve', 4076),
    ('AIR_NATIONAL_GUARD', 'Air National Guard', 4079),
    ('AIR_FORCE_RESERVE', 'Air Force Reserve', 4080),
    ('NAVY_RESERVE', 'Navy Reserve', 4078),
    ('MARINE_CORPS_RESERVE', 'Marine Corps Forces Reserve', 4077),
    ('COAST_GUARD_RESERVE', 'Coast Guard Reserve', 4081)
ON CONFLICT (code) DO NOTHING;

-- ============================================
-- 3. VETERANS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS public.veterans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    birth_date DATE,
    branch_code TEXT REFERENCES public.military_branches(code),
    military_status TEXT CHECK (military_status IN ('ACTIVE_DUTY', 'VETERAN', 'RESERVE', 'RETIRED')),
    discharge_date DATE,
    rank TEXT,
    service_number TEXT,
    source TEXT CHECK (source IN ('MANUAL', 'VA_GRAVE', 'VA_VLM', 'VA_ARMY', 'SHEERID')),
    source_id TEXT,
    metadata JSONB DEFAULT '{}',
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 4. VERIFICATIONS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS public.verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES public.profiles(id) ON DELETE CASCADE,
    veteran_id UUID REFERENCES public.veterans(id) ON DELETE SET NULL,
    
    -- SheerID specific
    sheerid_verification_id TEXT,
    sheerid_program_id TEXT,
    
    -- Service info
    service_type TEXT NOT NULL CHECK (service_type IN ('chatgpt', 'spotify', 'youtube', 'google_one', 'other')),
    
    -- Status tracking
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'approved', 'rejected', 'document_required', 'error', 'expired')),
    
    -- Request/Response data
    request_data JSONB DEFAULT '{}',
    response_data JSONB DEFAULT '{}',
    
    -- Document upload
    document_url TEXT,
    document_type TEXT CHECK (document_type IN ('DD214', 'MILITARY_ID', 'VA_CARD', 'OTHER')),
    
    -- Error tracking
    error_code TEXT,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    submitted_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ
);

-- ============================================
-- 5. VA LOOKUP CACHE TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS public.va_lookup_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL CHECK (source IN ('grave_locator', 'vlm', 'army_explorer')),
    search_query TEXT NOT NULL,
    search_params JSONB DEFAULT '{}',
    results JSONB DEFAULT '[]',
    result_count INTEGER DEFAULT 0,
    expires_at TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days'),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Unique constraint for caching
CREATE UNIQUE INDEX IF NOT EXISTS idx_va_cache_unique 
    ON public.va_lookup_cache(source, search_query);

-- ============================================
-- 6. API REQUEST LOGS TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS public.api_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.profiles(id) ON DELETE SET NULL,
    
    -- Request info
    endpoint TEXT NOT NULL,
    method TEXT NOT NULL,
    request_headers JSONB,
    request_body JSONB,
    
    -- Response info
    response_status INTEGER,
    response_body JSONB,
    
    -- Client info
    ip_address INET,
    user_agent TEXT,
    
    -- Performance
    duration_ms INTEGER,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 7. INDEXES
-- ============================================
CREATE INDEX IF NOT EXISTS idx_profiles_api_key ON public.profiles(api_key);
CREATE INDEX IF NOT EXISTS idx_profiles_email ON public.profiles(email);

CREATE INDEX IF NOT EXISTS idx_veterans_name ON public.veterans(first_name, last_name);
CREATE INDEX IF NOT EXISTS idx_veterans_user ON public.veterans(user_id);
CREATE INDEX IF NOT EXISTS idx_veterans_branch ON public.veterans(branch_code);
CREATE INDEX IF NOT EXISTS idx_veterans_source ON public.veterans(source);

CREATE INDEX IF NOT EXISTS idx_verifications_user ON public.verifications(user_id);
CREATE INDEX IF NOT EXISTS idx_verifications_status ON public.verifications(status);
CREATE INDEX IF NOT EXISTS idx_verifications_service ON public.verifications(service_type);
CREATE INDEX IF NOT EXISTS idx_verifications_sheerid ON public.verifications(sheerid_verification_id);
CREATE INDEX IF NOT EXISTS idx_verifications_created ON public.verifications(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_va_cache_source ON public.va_lookup_cache(source);
CREATE INDEX IF NOT EXISTS idx_va_cache_expires ON public.va_lookup_cache(expires_at);

CREATE INDEX IF NOT EXISTS idx_api_logs_user ON public.api_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_api_logs_endpoint ON public.api_logs(endpoint);
CREATE INDEX IF NOT EXISTS idx_api_logs_created ON public.api_logs(created_at DESC);

-- ============================================
-- 8. ROW LEVEL SECURITY (RLS)
-- ============================================

-- Enable RLS on all tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.veterans ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.verifications ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.va_lookup_cache ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.api_logs ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile" ON public.profiles
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

-- Veterans policies
CREATE POLICY "Users can view own veterans" ON public.veterans
    FOR SELECT USING (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can insert veterans" ON public.veterans
    FOR INSERT WITH CHECK (auth.uid() = user_id OR user_id IS NULL);

CREATE POLICY "Users can update own veterans" ON public.veterans
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own veterans" ON public.veterans
    FOR DELETE USING (auth.uid() = user_id);

-- Verifications policies
CREATE POLICY "Users can view own verifications" ON public.verifications
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert verifications" ON public.verifications
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own verifications" ON public.verifications
    FOR UPDATE USING (auth.uid() = user_id);

-- VA Cache policies (public read, authenticated insert)
CREATE POLICY "Anyone can view cache" ON public.va_lookup_cache
    FOR SELECT USING (true);

CREATE POLICY "Authenticated users can insert cache" ON public.va_lookup_cache
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- API Logs policies
CREATE POLICY "Users can view own logs" ON public.api_logs
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "System can insert logs" ON public.api_logs
    FOR INSERT WITH CHECK (true);

-- ============================================
-- 9. UPDATE TIMESTAMP FUNCTION
-- ============================================
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to tables with updated_at
CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_veterans_updated_at
    BEFORE UPDATE ON public.veterans
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- ============================================
-- 10. STORAGE BUCKET FOR DOCUMENTS
-- ============================================
-- Run this separately in Supabase Dashboard or via API:
-- INSERT INTO storage.buckets (id, name, public) VALUES ('documents', 'documents', false);

-- Storage policies (run in Supabase Dashboard):
-- CREATE POLICY "Users can upload documents" ON storage.objects
--     FOR INSERT WITH CHECK (bucket_id = 'documents' AND auth.uid()::text = (storage.foldername(name))[1]);
-- CREATE POLICY "Users can view own documents" ON storage.objects
--     FOR SELECT USING (bucket_id = 'documents' AND auth.uid()::text = (storage.foldername(name))[1]);

-- ============================================
-- DONE! Database schema created successfully.
-- ============================================
