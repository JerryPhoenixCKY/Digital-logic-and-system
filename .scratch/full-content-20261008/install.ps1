$ErrorActionPreference = 'Stop'
$taskRoot = (Get-Location).Path
$taskWork = Join-Path $taskRoot '.scratch\full-content-20261008'
$taskLive = [IO.Path]::GetFullPath((Join-Path $taskRoot 'Notes'))
$taskReady = [IO.Path]::GetFullPath((Join-Path $taskWork 'install-Notes'))
$taskBackup = [IO.Path]::GetFullPath((Join-Path $taskWork 'before-Notes'))
$taskPrefix = $taskRoot.TrimEnd('\') + '\'
foreach ($taskPath in @($taskLive, $taskReady, $taskBackup)) {
    if (-not $taskPath.StartsWith($taskPrefix, [StringComparison]::OrdinalIgnoreCase)) { throw 'A move target is outside this vault' }
}
if (Test-Path -LiteralPath $taskBackup) { throw 'The preserved Notes directory already exists; inspect before retrying' }
if ((Get-Item -LiteralPath $taskLive).LinkType) { throw 'Notes is a linked directory; inspect before writing' }
$taskPreflight = Get-Content -LiteralPath (Join-Path $taskWork 'pre-install-check.json') -Raw | ConvertFrom-Json
$taskExpectedFiles = @($taskPreflight.current_hashes.PSObject.Properties)
if (@(Get-ChildItem -LiteralPath $taskLive -Force).Count -ne $taskExpectedFiles.Count) { throw 'Notes directory changed after preflight' }
foreach ($taskFile in $taskExpectedFiles) {
    $taskHash = (Get-FileHash -LiteralPath (Join-Path $taskLive $taskFile.Name) -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($taskHash -ne $taskFile.Value) { throw ('A note changed after preflight: ' + $taskFile.Name) }
}
$taskPrepared = @(Get-ChildItem -LiteralPath $taskReady -File -Filter '*.md')
if ($taskPrepared.Count -ne 33) { throw 'Prepared notes are incomplete' }
foreach ($taskFile in $taskPrepared) {
    if (-not (Test-Path -LiteralPath (Join-Path $taskLive $taskFile.Name))) { throw ('Unexpected new filename: ' + $taskFile.Name) }
}
New-Item -ItemType Directory -Path $taskBackup | Out-Null
foreach ($taskFile in $taskExpectedFiles) {
    Copy-Item -LiteralPath (Join-Path $taskLive $taskFile.Name) -Destination (Join-Path $taskBackup $taskFile.Name)
}
$taskExtraArchive = [IO.Path]::GetFullPath((Join-Path $taskWork 'retired-extra-notes'))
if (-not $taskExtraArchive.StartsWith($taskPrefix, [StringComparison]::OrdinalIgnoreCase)) { throw 'Extra archive is outside this vault' }
New-Item -ItemType Directory -Path $taskExtraArchive | Out-Null
try {
    foreach ($taskFile in $taskPrepared) {
        Copy-Item -LiteralPath $taskFile.FullName -Destination (Join-Path $taskLive $taskFile.Name) -Force
    }
    foreach ($taskFile in $taskExpectedFiles) {
        if ($taskFile.Name -notin $taskPrepared.Name) {
            Move-Item -LiteralPath (Join-Path $taskLive $taskFile.Name) -Destination (Join-Path $taskExtraArchive $taskFile.Name)
        }
    }
} catch {
    foreach ($taskFile in $taskExpectedFiles) {
        Copy-Item -LiteralPath (Join-Path $taskBackup $taskFile.Name) -Destination (Join-Path $taskLive $taskFile.Name) -Force
    }
    throw
}
Write-Output 'Installed 31 topic notes and 2 navigation notes; all 35 previous files are preserved in before-Notes.'
