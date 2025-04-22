@echo off
setlocal enabledelayedexpansion
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management" /v DisablePagingExecutive /t REG_DWORD /d 1 /f
sc create CerebraCore binPath= "%cd%\cerebra.sys" type= kernel start= auto
sc start CerebraCore
for /l %%x in (1, 1, 12) do (
   start /node %%x /affinity 0x8000 python -c "from reality_hack import RealityHack; RealityHack()"
)
python -c "from cerebra_core import CerebraCore; cc = CerebraCore('model.bin'); print(cc)"
