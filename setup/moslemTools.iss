#define MyAppName "moslemTools"
#define MyAppVersion "8.1.0"
#define MyAppPublisher "mister anas , abd el-rahman mohammed alcoder"
#define MyAppURL "https://github.com/mesteranas/moslemTools_GUI/"
#define MyAppExeName "moslem_tools.exe"

[Setup]
AppName={#MyAppName}
AppId={{B1A04228-9227-4658-8536-AF1D4C6D1F55}}
AppVersion={#MyAppVersion }
;AppVersion={#MyAppVersion}
VersionInfoDescription=moslemTools , the best program for moslems
AppPublisher={#MyAppPublisher }
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher }
VersionInfoCopyright=copyright, ©2025 moslem tools developers
VersionInfoProductName=moslemTools
VersionInfoProductVersion={#MyAppVersion}
VersionInfoOriginalFileName=moslemTools_Setup.exe
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
ArchitecturesAllowed=x64
SetupIconFile=data\icons\app_icon.ico
DefaultDirName={sd}\program files\{#MyAppName}
DisableProgramGroupPage=yes
PrivilegesRequired=admin
OutputDir=moslemTools_build
OutputBaseFilename=moslemToolsSetup
LicenseFile=data\help\LICENSE.txt
Compression=lzma
CloseApplications=force
restartApplications=yes
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=no

ArchitecturesInstallIn64BitMode=x64
MinVersion=0,6.2
[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
[CustomMessages]
english.DeleteDataPrompt=Do you want to delete the settings and the downloaded data?

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"
[Files]
Source: "moslemTools_build\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "moslemTools_build\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\moslemTools"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\data\icons\app_icon.ico"
Name: "{autodesktop}\moslemTools"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\data\icons\app_icon.ico"; Tasks: desktopicon

[UninstallRun]
Filename: "taskkill"; Parameters: "/F /IM moslem_tools.exe"; Flags: runhidden

[UninstallDelete]
Type: filesandordirs; Name: "{pf}\moslemTools"

[InstallDelete]
Type: filesandordirs; Name: "{app}\*"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;


procedure CurStepChanged(CurStep: TSetupStep);
begin
end;

procedure DeleteSettingsFolder();
begin
  DelTree(ExpandConstant('{userappdata}\moslemTools_GUI'), True, True, True);
end;

function AskDeleteSettingsFolder(): Boolean;
begin
  Result := MsgBox(ExpandConstant('{cm:DeleteDataPrompt}'), mbConfirmation, MB_YESNO) = IDYES;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    if AskDeleteSettingsFolder() then
    begin
      DeleteSettingsFolder();
    end;
  end;
end;

