<#
.SYNOPSIS
    Provisionne une base PostgreSQL locale pour PancreaCare et y charge le schema.
    Ne modifie AUCUN fichier du projet.
#>

[CmdletBinding()]
param(
    [string]$DbName        = "pancreacare",
    [string]$DbUser        = "pancreacare",
    [string]$DbPassword    = $null,
    [int]    $Port         = 5432,
    [string]$AdminPassword = $null,
    [switch]$AutoInstall
)

$ErrorActionPreference = "Stop"
$ProgressPreference    = "SilentlyContinue"

$Backend = "C:\Users\INFO\Desktop\CHU stage\Pancrea-care\backend"
$Schema  = Join-Path $Backend "database\pancra_db_schema_supabase.sql"
$MigDir  = Join-Path $Backend "database\migrations"

$script:Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Say   { param($m) Write-Host $m }
function Ok    { param($m) Write-Host "  [OK]      $m" -ForegroundColor Green }
function Err   { param($m) Write-Host "  [ERREUR]  $m" -ForegroundColor Red }
function Warn  { param($m) Write-Host "  [ATTENTION] $m" -ForegroundColor Yellow }
function Etape { param($m) Write-Host "`n=== $m ===" -ForegroundColor Cyan }

function Invoke-Sql {
    param(
        [Parameter(Mandatory)][string]$Sql,
        [string]$Database = "postgres",
        [switch]$Silence
    )
    # Le SQL passe par un fichier temporaire UTF-8 sans BOM : transmettre du SQL
    # contenant des guillemets en argument natif est une source de corruption
    # silencieuse sous PowerShell.
    $tmp = [System.IO.Path]::GetTempFileName()
    [System.IO.File]::WriteAllText(
        $tmp, "\set ON_ERROR_STOP on`n" + $Sql, $script:Utf8NoBom
    )
    # psql ecrit ses erreurs sur stderr ; sous $ErrorActionPreference = "Stop",
    # toute sortie stderr deviendrait une erreur terminante. On isole stderr dans
    # un fichier pour ne garder sur stdout que le resultat de la requete.
    $errFile = [System.IO.Path]::GetTempFileName()
    $prec = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $sortie = & $psql -U postgres -h localhost -p $Port -d $Database -tA -q -f $tmp 2>$errFile
    $code   = $LASTEXITCODE
    $ErrorActionPreference = $prec
    $erreurs = Get-Content -LiteralPath $errFile -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $tmp, $errFile -Force -ErrorAction SilentlyContinue

    if (-not $Silence) {
        foreach ($ligne in $erreurs) {
            if ("$ligne" -match "ERROR|FATAL|ERREUR") { Err $ligne }
        }
    }
    return (($sortie -join "`n").Trim())
}

function Find-Psql {
    $dansChemin = Get-Command psql -ErrorAction SilentlyContinue
    if ($dansChemin) { return $dansChemin.Source }

    foreach ($base in @("C:\Program Files\PostgreSQL", "C:\Program Files (x86)\PostgreSQL")) {
        if (-not (Test-Path $base)) { continue }
        foreach ($v in (Get-ChildItem $base -Directory | Sort-Object Name -Descending)) {
            $candidat = Join-Path $v.FullName "bin\psql.exe"
            if (Test-Path $candidat) { return $candidat }
        }
    }
    return $null
}

# --- 1. Localiser psql -------------------------------------------------------
Etape "1/6  Verification de PostgreSQL"
$psql = Find-Psql

if (-not $psql -and $AutoInstall) {
    Say "PostgreSQL absent, installation via winget..."
    winget install --id PostgreSQL.PostgreSQL --silent `
        --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { Err "winget a echoue"; exit 1 }
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("Path", "User")
    $psql = Find-Psql
}

if (-not $psql) {
    Err "PostgreSQL est introuvable (psql.exe)."
    Say "  winget install --id PostgreSQL.PostgreSQL"
    exit 2
}
Ok "psql : $psql"
& $psql --version

# --- 2. Serveur --------------------------------------------------------------
Etape "2/6  Serveur"
$service = Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue |
           Sort-Object Name -Descending | Select-Object -First 1

if ($service -and $service.Status -ne "Running") {
    try { Start-Service $service.Name -ErrorAction Stop; Ok "service demarre" }
    catch { Warn "demarrage impossible : $($_.Exception.Message)" }
}

if (-not $AdminPassword) {
    Say ""
    Say "Mot de passe du role administrateur 'postgres' (Entree si aucun) :"
    $AdminPassword = Read-Host
}
$env:PGPASSWORD       = $AdminPassword
$env:PGCLIENTENCODING = "UTF8"

if ((Invoke-Sql "SELECT 1" -Silence) -ne "1") {
    Err "Connexion refusee sur localhost:$Port avec le role 'postgres'."
    exit 3
}
Ok "connexion etablie sur localhost:$Port"

# --- 3. Role applicatif ------------------------------------------------------
Etape "3/6  Role applicatif '$DbUser'"
$genere = $false
if (-not $DbPassword) {
    $octets = New-Object byte[] 18
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($octets)
    $DbPassword = ([System.BitConverter]::ToString($octets) -replace '-', '').ToLower()
    $genere = $true
} elseif ($DbPassword -match '[@:/ ?#\[\]%]') {
    Err "Mot de passe incompatible avec une URL de connexion."
    exit 4
}

if ((Invoke-Sql "SELECT 1 FROM pg_roles WHERE rolname = '$DbUser'" -Silence) -ne "1") {
    Invoke-Sql "CREATE ROLE ""$DbUser"" LOGIN PASSWORD '$DbPassword'" -Silence | Out-Null
    Ok "role cree"
} else {
    Invoke-Sql "ALTER ROLE ""$DbUser"" LOGIN PASSWORD '$DbPassword'" -Silence | Out-Null
    Ok "role existant, mot de passe mis a jour"
}

# --- 4. Base -----------------------------------------------------------------
Etape "4/6  Base '$DbName'"
if ((Invoke-Sql "SELECT 1 FROM pg_database WHERE datname = '$DbName'" -Silence) -ne "1") {
    # CREATE DATABASE ne peut pas s'executer dans une transaction.
    Invoke-Sql "CREATE DATABASE ""$DbName"" OWNER ""$DbUser"" ENCODING 'UTF8'" -Silence | Out-Null
    Ok "base creee"
} else {
    Ok "base deja presente"
}

# --- 5. Schema ---------------------------------------------------------------
Etape "5/6  Schema de base"
if (-not (Test-Path $Schema)) { Err "Introuvable : $Schema"; exit 5 }
$dejaTables = (Invoke-Sql "SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'" -Database $DbName -Silence).Trim()
if ($dejaTables -ne "0") {
    Ok "schema de base deja present ($dejaTables tables)"
} else {
    $prec = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $env:PGPASSWORD = $DbPassword
    & $psql -U $DbUser -h localhost -p $Port -d $DbName -v ON_ERROR_STOP=1 -q -f $Schema 2>&1 |
        ForEach-Object { if ("$_" -match "ERROR|FATAL|ERREUR") { Err $_ } }
    $code = $LASTEXITCODE
    $env:PGPASSWORD = $AdminPassword
    $ErrorActionPreference = $prec
    if ($code -ne 0) { Err "schema de base : echec"; exit 6 }
    Ok "schema de base applique"
}

# --- 6. Migrations -----------------------------------------------------------
Etape "6/6  Migrations"
$prec = $ErrorActionPreference
$ErrorActionPreference = "Continue"
$migrations = @()
if (Test-Path $MigDir) {
    $migrations = Get-ChildItem -Path $MigDir -Filter "*.sql" | Sort-Object Name
}
$env:PGPASSWORD = $DbPassword
foreach ($m in $migrations) {
    & $psql -U $DbUser -h localhost -p $Port -d $DbName -v ON_ERROR_STOP=1 -q -f $m.FullName 2>&1 |
        ForEach-Object { if ("$_" -match "ERROR|FATAL|ERREUR") { Err $_ } }
    $code = $LASTEXITCODE
    if ($code -ne 0) { $env:PGPASSWORD = $AdminPassword; $ErrorActionPreference = $prec; Err "migration en echec : $($m.Name)"; exit 7 }
    Ok $m.Name
}
$env:PGPASSWORD = $AdminPassword
$ErrorActionPreference = $prec

# --- Verification ------------------------------------------------------------
Etape "Verification"
$nb = Invoke-Sql "SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'" -Database $DbName -Silence
Write-Host "  tables creees : $nb"

$manquantes = @()
foreach ($t in @("patient", "medecin", "dossier_patient", "evaluation_clinique", "compte")) {
    $trouvee = Invoke-Sql "SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_name='$t'" -Database $DbName -Silence
    if ("$trouvee".Trim() -eq "0") { $manquantes += $t }
}
if ($manquantes.Count -gt 0) { Err "tables manquantes : $($manquantes -join ', ')"; exit 8 }
Ok "tables essentielles presentes"

$url = "postgresql://$DbUser" + ":" + $DbPassword + "@localhost:$Port/$DbName"
Etape "Termine"
Say ""
Say "A reporter dans backend\.env :"
Write-Host "    DATABASE_URL=$url" -ForegroundColor Yellow
if ($genere) { Warn "Mot de passe genere : $DbPassword" }
Say ""
Say "  1. Recopier le DATABASE_URL dans backend\.env"
Say "  2. cd backend"
Say "  3. python -m app.bootstrap_admin"
Say "  4. python -m uvicorn app.main:app --reload --port 8000"
