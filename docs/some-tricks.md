# Some Tricks

95 entries.

## Windows Ring0

- [https://www.unknowncheats.me/forum/general-programming-and-reversing/495279-messagebox-kernel-mode.html](https://www.unknowncheats.me/forum/general-programming-and-reversing/495279-messagebox-kernel-mode.html) — Msgbox
- [https://back.engineering/01/12/2020/](https://back.engineering/01/12/2020/) — Page Table Manipulation
- [https://git.back.engineering/_xeroxz/PSKP](https://git.back.engineering/_xeroxz/PSKP) — PTE Hook
- [Rythorndoran/PageTableHook](https://github.com/Rythorndoran/PageTableHook) — PTE Hook
- [stdhu/windows-kernel-pagehook](https://github.com/stdhu/windows-kernel-pagehook) — PTE Hook
- [Xyrem/Yumekage](https://github.com/Xyrem/Yumekage) — PTE Hook
- [brew02/FastPFHook](https://github.com/brew02/FastPFHook) — PF Hook
- [gmh5225/Allocating-individual-pages](https://github.com/gmh5225/Allocating-individual-pages) — MmAllocateIndependentPagesEx `mirror`
- [gmh5225/Hook-HvlSwitchVirtualAddressSpace](https://github.com/gmh5225/Hook-HvlSwitchVirtualAddressSpace) — HvcallCodeVa `mirror`
- [1401199262/HookHvcallCodeVa](https://github.com/1401199262/HookHvcallCodeVa) — HvcallCodeVa
- [gmh5225/Driver-HypercallPageHook](https://github.com/gmh5225/Driver-HypercallPageHook) — HvcallCodeVa `mirror`
- [Xyrem/HyperDeceit](https://github.com/Xyrem/HyperDeceit) — HvcallCodeVa
- [gmh5225/CallMeWin32kDriver](https://github.com/gmh5225/CallMeWin32kDriver) — Load your driver like win32k.sys `mirror`
- [gmh5225/DSEDodge-Signed-Kernel-Driver](https://github.com/gmh5225/DSEDodge-Signed-Kernel-Driver) — Leveraging PTT to defeat DSE `mirror`
- [wbenny/KSOCKET](https://github.com/wbenny/KSOCKET) — Kernel Berkeley socket
- [StephanvanSchaik/windows-kernel-rs](https://github.com/StephanvanSchaik/windows-kernel-rs) — Writing Windows kernel drivers in Rust
- [rbmm/KPDB](https://github.com/rbmm/KPDB) — Parsing PDB in Driver
- [GetRektBoy724/KPDB](https://github.com/GetRektBoy724/KPDB) — Parsing PDB in Driver
- [gmh5225/FakeEnclave](https://github.com/gmh5225/FakeEnclave) — A poc that abuses Enclave `mirror`
- [gmh5225/LetMeGG](https://github.com/gmh5225/LetMeGG) — A POC about how to prevent windbg break `mirror`
- [UCFoxi/NotifyRoutineHijackThread](https://github.com/UCFoxi/NotifyRoutineHijackThread) — Hijack PspCreateThreadNotifyRoutine
- [GetWindowName In Kernel Mode](https://www.unknowncheats.me/forum/anti-cheat-bypass/517022-getwindowname-kernel-mode.html)
- [GetWindowInfo In Kernel Mode](https://www.unknowncheats.me/forum/anti-cheat-bypass/519261-getwindowinfo.html)
- [Hook KdTrap(Windows global exception hander)](https://www.unknowncheats.me/forum/anti-cheat-bypass/500156-hook-kdtrap-windows-global-exception-hander.html) — Hook KdTrap
- [gmh5225/Hook-KdTrap](https://github.com/gmh5225/Hook-KdTrap) — Hook KdTrap `mirror`
- [SamuelTulach/HookGuard](https://github.com/SamuelTulach/HookGuard) — Global exception/KdpDebugRoutineSelect
- [1401199262/HookSwapContext](https://github.com/1401199262/HookSwapContext) — SwapContext hook
- [gmh5225/Driver-SoulExtraction](https://github.com/gmh5225/Driver-SoulExtraction) — Extracting cert information `mirror`
- [Ido-Moshe-Github/CiDllDemo](https://github.com/Ido-Moshe-Github/CiDllDemo) — Use ci.dll API for validating Authenticode signature of files
- [mihaly044/pedigest](https://github.com/mihaly044/pedigest) — Calculating the authenticode digest
- [NSG650/Bad-BugCheck-Old](https://github.com/NSG650/Bad-BugCheck-Old) — BSOD
- [NSG650/Bad-Bugcheck](https://github.com/NSG650/Bad-Bugcheck) — BSOD
- [NSG650/NoMoreBugCheck](https://github.com/NSG650/NoMoreBugCheck) — BSOD
- [NSG650/BugCheckHack](https://github.com/NSG650/BugCheckHack) — BSOD
- [NSG650/BugCheck2Linux](https://github.com/NSG650/BugCheck2Linux) — BSOD
- [AnalogFeelings/KmdfMandelcheck](https://github.com/AnalogFeelings/KmdfMandelcheck) — BSOD
- [XaFF-XaFF/BugcheckSuppressor](https://github.com/XaFF-XaFF/BugcheckSuppressor) — HVCI/kCET-aware bugcheck suppressor PoC via data-only HAL dispatch hook + RtlUnwindEx recovery
- [stuxnet147/PiDqSerializationWrite-Example](https://github.com/stuxnet147/PiDqSerializationWrite-Example) — PiDqSerializationWrite
- [Rythorndoran/enum_real_dirbase](https://github.com/Rythorndoran/enum_real_dirbase) — Find real dirbase
- [backengineering/POC-ExFlushTb](https://github.com/backengineering/POC-ExFlushTb) — A POC for monitoring Tb
- [https://gist.github.com/gmh5225/ab00f831ffdf4ef608ab3b6eb0d37250](https://gist.github.com/gmh5225/ab00f831ffdf4ef608ab3b6eb0d37250) — Create process from KernelMode via APC
- [SamuelTulach/PwnedBoot](https://github.com/SamuelTulach/PwnedBoot) — Using Windows' own bootloader as a shim to bypass Secure Boot
- [Th3Spl/IoCreateDriver](https://github.com/Th3Spl/IoCreateDriver) — IoCreateDriver Implementation
- [r0keb/Smep-Bypass](https://github.com/r0keb/Smep-Bypass) — Various techniques used to bypass SMEP in the Windows Kernel
- [brew02/CovertThread](https://github.com/brew02/CovertThread) — Creating covert system threads on Windows by leveraging the page tables and IDT

## Windows Ring3

- [https://secret.club/2021/01/04/thread-stuff.html](https://secret.club/2021/01/04/thread-stuff.html) — Anti Debug
- [Sentient111/StealingSignatures](https://github.com/Sentient111/StealingSignatures) — Stealing signatures from pe files
- [secretsquirrel/SigThief](https://github.com/secretsquirrel/SigThief) — Stealing signatures from pe files
- [dslee2022/SignatureKid](https://github.com/dslee2022/SignatureKid) — Stealing signatures from pe files
- [jfmaes/LazySign](https://github.com/jfmaes/LazySign) — Fake Cert
- [Tylous/Limelighter](https://github.com/Tylous/Limelighter) — Fake Cert
- [gmh5225/FakeSign](https://github.com/gmh5225/FakeSign) — Fake Cert `mirror`
- [Adepts-Of-0xCC/MiniDumpWriteDumpPoC](https://github.com/Adepts-Of-0xCC/MiniDumpWriteDumpPoC) — Dump Memory
- [A x64 Write-What-Where exploit+shellcode execution vulnerability](https://www.unknowncheats.me/forum/anti-cheat-bypass/503519-wwwaryasinject-x64-write-exploit-shellcode-execution-vulnerability.html)
- [Dll injection through code page id modification in registry](https://github.com/gmh5225/NlsCodeInjectionThroughRegistry) `mirror`
- [huoji120/Etw-Syscall](https://github.com/huoji120/Etw-Syscall) — ETW Syscall
- [ekknod/SetWindowHookEx](https://github.com/ekknod/SetWindowHookEx) — Using SetWindowHookEx for preinjected DLL's
- [A tool for patching authenticode signed PE files (exe, dll, sys ..etc) without invalidating or breaking the existing signature](https://github.com/med0x2e/SigFlip)
- [Simple program to stream offsets for your game cheat](https://github.com/gmh5225/OffsetStreaming) `mirror`
- [jnastarot/HIGU_ntcall](https://github.com/jnastarot/HIGU_ntcall) — Direct System Calls
- [SilentisVox/DoomSyscalls](https://github.com/SilentisVox/DoomSyscalls) — Indirect syscalls: dynamic SSN and syscall-instruction resolve; return-address spoof via ntdll gadgets; userland hook / RIP-return evasion research
- [EvilBytecode/IDontLikeFileLocks](https://github.com/EvilBytecode/IDontLikeFileLocks) — Dump locked files by stealing memory-mapped section handle
- [A kernel exploit leveraging NtUserHardErrorControl to elevate a thread to KernelMode and achieve arbitrary kernel R/W & more](https://github.com/gmh5225/ANGRYORCHARD) `mirror`
- [Running Shellcode Through EnumDisplayMonitors](https://marcoramilli.com/2022/06/15/running-shellcode-through-windows-callbacks/?utm_source=twitter&utm_medium=social&utm_campaign=ReviveOldPost)
- [open-source windows defender manager can disable windows defender permanently](https://github.com/qtkite/defender-control)
- [Read Memory without ReadProcessMemory for Current Process](https://github.com/gmh5225/CReadMemory) `mirror`
- [get process token whose integrity level is system and manipulate it to get privilege escalation](https://github.com/gmh5225/manipulating_token) `mirror`
- [A library that meant to perform evasive communication using stolen browser socket](https://github.com/Idov31/Venom)
- [cpz/trinity](https://github.com/cpz/trinity) — Fully disables & removes Windows Defender
- [gmh5225/Disable-Windows-Defender-](https://github.com/gmh5225/Disable-Windows-Defender-) — Disable Windows Defender `mirror`
- [gmh5225/r0ak](https://github.com/gmh5225/r0ak) — r0ak `mirror`
- [gmh5225/Wizard-Loader](https://github.com/gmh5225/Wizard-Loader) — Abuse Xwizard.exe for DLL Side-Loading `mirror`
- [LloydLabs/shellcode-plain-sight](https://github.com/LloydLabs/shellcode-plain-sight) — Hiding shellcode in plain sight within a large memory region
- [huntandhackett/process-cloning](https://github.com/huntandhackett/process-cloning) — Clone process
- [backengineering/msrexec](https://github.com/backengineering/msrexec) — Elevate arbitrary MSR writes to kernel execution
- [mandiant/ShimCacheParser](https://github.com/mandiant/ShimCacheParser) — Shim Cache parser
- [gmh5225/pmctrace](https://github.com/gmh5225/pmctrace) — Real-time collection of PMCs via ETW `mirror`
- [Idov31/EtwLeakKernel](https://github.com/Idov31/EtwLeakKernel) — Leaking kernel addresses from ETW consumers. Requires Administrator privileges
- [SamuelTulach/SecureGame](https://github.com/SamuelTulach/SecureGame) — POC game using VBS enclaves to protect itself from cheating
- [Teach2Breach/moonwalk](https://github.com/Teach2Breach/moonwalk) — find dll base addresses without PEB WALK
- [brew02/MountSystemPartition](https://github.com/brew02/MountSystemPartition) — Mounting the system partition on Windows
- [LloydLabs/delete-self-poc](https://github.com/LloydLabs/delete-self-poc) — A way to delete a locked file, or current running executable, on disk
- [unkvolism/Solemn](https://github.com/unkvolism/Solemn) — A command-line tool for Windows that automates adding drivers to the HVCI (HvciDisallowedImages) custom blocklist
- [2x7EQ13/CreateProcessAsPPL](https://github.com/2x7EQ13/CreateProcessAsPPL) — This is the loader that supports running a program with Protected Process Light (PPL) protection functionality
- [Peribunt/VPGATHER](https://github.com/Peribunt/VPGATHER) — Using the peculiar behaviour of the VPGATHER instructions to determine if an address will fault before it is truly accessed

## Linux

- [MatheuZSecurity/RingReaper](https://github.com/MatheuZSecurity/RingReaper) — Linux post-exploitation agent that uses io_uring to stealthily bypass EDR detection by avoiding traditional syscalls
- [boratanrikulu/gecit](https://github.com/boratanrikulu/gecit) — DPI bypass research tool: fake TLS ClientHello desync + built-in DoH; eBPF sock_ops on Linux, TUN proxy on macOS/Windows

## Android

- [WindySha/bypassHiddenApiRestriction](https://github.com/WindySha/bypassHiddenApiRestriction) — Bypass hidden api restriction
- [LSPosed/AndroidHiddenApiBypass](https://github.com/LSPosed/AndroidHiddenApiBypass) — Bypass hidden api restriction
- [stars-one/ASCTool](https://github.com/stars-one/ASCTool) — Apk Signature Crack Tool
- [ekknod/usbsn](https://github.com/ekknod/usbsn) — USB serial number changer (root only)
- [gmh5225/Android-privilege-CVE-2022-20452-LeakValue](https://github.com/gmh5225/Android-privilege-CVE-2022-20452-LeakValue) — Privilege Escalation `mirror`
- [MlgmXyysd/KernelSU_Debug](https://github.com/MlgmXyysd/KernelSU_Debug) — KernelSU modified for debugging
- [CoolestEnoch/kernel-su-huawei-nova2](https://github.com/CoolestEnoch/kernel-su-huawei-nova2) — KernelSU for huawei
- [gmh5225/android_kernel_huawei_hi6250-8_Exp](https://github.com/gmh5225/android_kernel_huawei_hi6250-8_Exp) — KernelSU for huawei `mirror`
