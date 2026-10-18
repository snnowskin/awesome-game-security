# Create the remote repository and push, once gh is authenticated.
# Kept as a file so the post-auth step is one command instead of five.
$ErrorActionPreference = 'Stop'
$env:HTTPS_PROXY = 'http://127.0.0.1:7890'
$env:HTTP_PROXY  = 'http://127.0.0.1:7890'
$env:NO_PROXY    = '127.0.0.1,localhost'
$gh = 'C:\Program Files\GitHub CLI\gh.exe'
$repo = if ($args.Count -gt 0) { $args[0] } else { 'awesome-game-security' }

& $gh auth status *> $null
if ($LASTEXITCODE -ne 0) { throw 'gh is not authenticated; run gh auth login first' }

$exists = & $gh repo view "snnowskin/$repo" --json name 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "remote $repo already exists, wiring it up"
} else {
    Write-Host "creating snnowskin/$repo"
    & $gh repo create "snnowskin/$repo" --public `
        --description 'Structured, linted index of game-security research: per-section docs, a JSON dataset, and AI-agent skills derived from gmh5225/awesome-game-security (MIT).'
}

git remote remove origin 2>$null
git remote add origin "git@github.com:snnowskin/$repo.git"
git push -u origin main
Write-Host '--- pushed ---'
git log --oneline -1
