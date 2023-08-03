import re

datas = [
    {
      "time": 1690881407.063548,
      "raw": " [ 08-01 18:16:48.589  3564: 3564 D/hal_frontpanel ]\nhal_frontpanel:HAL_FrontPanelSetLedState v102(3, 2)\n\n"
    },
    {
      "time": 1690881407.063599,
      "raw": " [ 08-01 18:16:48.605  3564:13947 W/RendererPolicyBase_0 ]\nvideo render: 59.94 fps, drop: 0.00 fps\n\n"
    },
    {
      "time": 1690881407.067277,
      "raw": " [ 08-01 18:16:48.691  3564: 3564 D/DEVICE   ]\nBTF|DEVICE_SetLedState|111|OUT| \n\n\n"
    },
    {
      "time": 1690881407.067309,
      "raw": " [ 08-01 18:16:48.691  2790: 2790 W/btvSocHalService-JNI ]\nbtvSocHalService_SetLedState::994 : out, opStatus:0 \n\n"
    },
    {
      "time": 1690881407.09759,
      "raw": " [ 08-01 18:16:48.692  4646: 4763 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState after jni, index: 3, status: 2, result: true\n\n"
    },
    {
      "time": 1690881407.097632,
      "raw": " [ 08-01 18:16:48.692  4646: 4763 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState take before ===============================================\n\n"
    },
    {
      "time": 1690881407.121232,
      "raw": " [ 08-01 18:16:48.721  3499: 3499 W/ATVRemoteAudioH ]\ntype=1400 audit(0.0:3675840): avc: denied { call } for scontext=u:r:hal_audio_amlogic:s0 tcontext=u:r:rc_server:s0 tclass=binder permissive=0\n\n"
    },
    {
      "time": 1690881407.299046,
      "raw": " [ 08-01 18:16:48.725  3499: 3745 W/ServiceManagement ]\ngetService: unable to call into hwbinder service for vendor.amlogic.hardware.remotecontrol@1.0::IRemoteControl/default.\n\n"
    },
    {
      "time": 1690881407.302461,
      "raw": " [ 08-01 18:16:48.749  3564:13946 I/LivePlayer_0 ]\nSEAN onCheckVoiceAssistant(mString: nugu_playback=off)\n\n"
    },
    {
      "time": 1690881407.302486,
      "raw": " [ 08-01 18:16:48.926  3587:15157 I/adbd     ]\nhost-66: write thread spawning\n\n"
    },
    {
      "time": 1690881407.3025,
      "raw": " [ 08-01 18:16:48.928  3587:15156 I/adbd     ]\nhost-66: read thread spawning\n\n"
    },
    {
      "time": 1690881407.302512,
      "raw": " [ 08-01 18:16:48.928  3587:15156 I/adbd     ]\nhost-66: read failed: Success\n\n"
    },
    {
      "time": 1690881407.302524,
      "raw": " [ 08-01 18:16:48.928  3587:15156 I/adbd     ]\nhost-66: connection terminated: read failed\n\n"
    },
    {
      "time": 1690881407.302536,
      "raw": " [ 08-01 18:16:48.928  3587: 3587 I/adbd     ]\nhost-66: already offline\n\n"
    },
    {
      "time": 1690881407.305201,
      "raw": " [ 08-01 18:16:48.928  3587: 3587 I/adbd     ]\ndestroying transport host-66\n\n"
    },
    {
      "time": 1690881407.305215,
      "raw": " [ 08-01 18:16:48.928  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-66): stopping\n\n"
    },
    {
      "time": 1690881407.305227,
      "raw": " [ 08-01 18:16:48.930  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-66): stopped\n\n"
    },
    {
      "time": 1690881407.382966,
      "raw": " [ 08-01 18:16:48.930  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-66): destructing\n\n"
    },
    {
      "time": 1690881407.406844,
      "raw": " [ 08-01 18:16:48.930  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-66): already stopped\n\n"
    },
    {
      "time": 1690881407.489283,
      "raw": " [ 08-01 18:16:49.010  2790:13944 D/BOXKEY-STDVB ]\n[DEVICE 0] ++ remain buffer size : 31584\n\n"
    },
    {
      "time": 1690881407.581056,
      "raw": " [ 08-01 18:16:49.034  3564:13967 I/HalAudioOutput ]\noutputRate:47997(1.00)\n\n"
    },
    {
      "time": 1690881407.62208,
      "raw": " [ 08-01 18:16:49.117  4490: 4490 D/MDNSService ]\nMDNSMsgHandler() AM_EVENT_CHECK_NETWORK_CONFIG. isConnected : true\n\n"
    },
    {
      "time": 1690881407.717896,
      "raw": " [ 08-01 18:16:49.209  3564:13953 I/MiniAmVideoDec_0 ]\nvbuf:976585/2097152, rp:0x6032849, latency:1234.57ms\n\n"
    },
    {
      "time": 1690881407.720797,
      "raw": " [ 08-01 18:16:49.250  3564:13946 I/LivePlayer_0 ]\nSEAN onCheckVoiceAssistant(mString: nugu_playback=off)\n\n"
    },
    {
      "time": 1690881407.745955,
      "raw": " [ 08-01 18:16:49.345  2790:13937 E/libc     ]\nAccess denied finding property \"skb.audio.output\"\n\n"
    },
    {
      "time": 1690881407.746004,
      "raw": " [ 08-01 18:16:49.341  2790: 2790 W/btvservice@1.0- ]\ntype=1400 audit(0.0:3675841): avc: denied { read } for name=\"u:object_r:default_prop:s0\" dev=\"tmpfs\" ino=189 scontext=u:r:btvservice_hal:s0 tcontext=u:object_r:default_prop:s0 tclass=file permissive=0\n\n"
    },
    {
      "time": 1690881407.746021,
      "raw": " [ 08-01 18:16:49.371  4405: 5509 D/iSQMSAgent_LogSystem ]\nCISQMSSystemInfo::check_system_status 0x0001\n\n\n"
    },
    {
      "time": 1690881407.746036,
      "raw": " [ 08-01 18:16:49.371  4405: 5509 D/iSQMSAgent_LogSystem ]\nCISQMSEnvm get_system_info - eType : 0\n\n\n"
    },
    {
      "time": 1690881407.746062,
      "raw": " [ 08-01 18:16:49.372  4405: 5509 D/iSQMSAgent_LogSystem ]\ncpu_usage=45 idle=12426  total=22397\n\n\n"
    },
    {
      "time": 1690881407.746078,
      "raw": " [ 08-01 18:16:49.372  4405: 5509 D/iSQMSAgent_LogSystem ]\nget_system_memory MEM total= 3063156 free= 258240 buffers =717952 cached=83136 current=69\n\n\n"
    },
    {
      "time": 1690881407.947437,
      "raw": " [ 08-01 18:16:49.372  4405: 5509 D/iSQMSAgent_LogSystem ]\nCISQMSEnvm get_system_info - eType : 1\n\n\n"
    },
    {
      "time": 1690881407.958871,
      "raw": " [ 08-01 18:16:49.372  4405: 5509 D/iSQMSAgent_LogSystem ]\nCISQMSSystemInfo::MEM Check memInfo.currentMem =69, limitMem=95\n\n\n"
    },
    {
      "time": 1690881407.961635,
      "raw": " [ 08-01 18:16:49.574 15158:15158 D/AndroidRuntime ]\n>>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<\n\n\n"
    },
    {
      "time": 1690881407.969072,
      "raw": " [ 08-01 18:16:49.586 15158:15158 I/AndroidRuntime ]\nUsing default boot image\n\n"
    },
    {
      "time": 1690881403.061985,
      "raw": " [ 08-01 18:16:44.496 15093:15093 I/app_process ]\nCore platform API reporting enabled, enforcing=false\n\n"
    },
    {
      "time": 1690881403.079955,
      "raw": " [ 08-01 18:16:44.600  3564:13947 W/RendererPolicyBase_0 ]\nvideo render: 59.87 fps, drop: 0.00 fps\n\n"
    },
    {
      "time": 1690881403.083727,
      "raw": " [ 08-01 18:16:44.689 15093:15093 D/ICU      ]\nTime zone APEX file found: /apex/com.android.tzdata/etc/icu/icu_tzdata.dat\n\n"
    },
    {
      "time": 1690881403.086421,
      "raw": " [ 08-01 18:16:44.707 15093:15093 W/app_process ]\nUsing default instruction set features for ARM CPU variant (cortex-a9) using conservative defaults\n\n"
    },
    {
      "time": 1690881403.086455,
      "raw": " [ 08-01 18:16:44.710 15093:15093 I/app_process ]\nThe ClassLoaderContext is a special shared library.\n\n"
    },
    {
      "time": 1690881403.116899,
      "raw": " [ 08-01 18:16:44.714  3499: 3745 W/ServiceManagement ]\ngetService: unable to call into hwbinder service for vendor.amlogic.hardware.remotecontrol@1.0::IRemoteControl/default.\n\n"
    },
    {
      "time": 1690881403.119621,
      "raw": " [ 08-01 18:16:44.709  3499: 3499 W/ATVRemoteAudioH ]\ntype=1400 audit(0.0:3675832): avc: denied { call } for scontext=u:r:hal_audio_amlogic:s0 tcontext=u:r:rc_server:s0 tclass=binder permissive=0\n\n"
    },
    {
      "time": 1690881403.132957,
      "raw": " [ 08-01 18:16:44.745  3564:13946 I/LivePlayer_0 ]\nSEAN onCheckVoiceAssistant(mString: nugu_playback=off)\n\n"
    },
    {
      "time": 1690881403.13474,
      "raw": " [ 08-01 18:16:44.746 15093:15093 W/app_process ]\nJNI RegisterNativeMethods: attempt to register 0 native methods for android.media.AudioAttributes\n\n"
    },
    {
      "time": 1690881403.136419,
      "raw": " [ 08-01 18:16:44.761 15093:15093 D/AndroidRuntime ]\nCalling main entry com.android.commands.input.Input\n\n"
    },
    {
      "time": 1690881403.138588,
      "raw": " [ 08-01 18:16:44.762 15093:15093 V/KeyEvent ]\n  keyCodeFromString ##2 keyCode: 82, LAST_KEYCODE : 454\n\n"
    },
    {
      "time": 1690881403.13861,
      "raw": " [ 08-01 18:16:44.764  3820:30268 D/WindowManager ]\ninterceptKeyTq keycode=82 interactive=true keyguardActive=false policyFlags=2b000000\n\n"
    },
    {
      "time": 1690881403.143481,
      "raw": " [ 08-01 18:16:44.765  3820: 3907 I/WindowManager ]\ninterceptKeyTi keyCode=82 down=true repeatCount=0 keyguardOn=false canceled=false policyFlags=1795162112 mDeviceId=-1 mSource=0 mScanCode=0 mCharacters=null\n\n"
    },
    {
      "time": 1690881403.143501,
      "raw": " [ 08-01 18:16:44.766  3820: 3907 D/WindowManager ]\ninterceptKeyTi strDate 2023-08-01 18:16\n\n"
    },
    {
      "time": 1690881403.143514,
      "raw": " [ 08-01 18:16:44.767  3820: 3907 D/WindowManager ]\ninterceptSkbFuctionKeyBeforeDispatching keycode = 82\n\n"
    },
    {
      "time": 1690881403.143526,
      "raw": " [ 08-01 18:16:44.767  3820: 3907 D/WindowManager ]\nkeycode : 82 - processed. by skb function key\n\n"
    },
    {
      "time": 1690881403.143538,
      "raw": " [ 08-01 18:16:44.767  3820: 3907 W/GlobalKeyManager ]\nhandleGlobalKey keyCode : 82 componentnull\n\n"
    },
    {
      "time": 1690881403.14355,
      "raw": " [ 08-01 18:16:44.767  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown start keyCode = 82, packageName: com.skb.tv\n\n"
    },
    {
      "time": 1690881403.143562,
      "raw": " [ 08-01 18:16:44.767  4186: 4186 W/BTV_IME-InputAttributes ]\nisAllowApp mInputType :0, TYPE_CLASS_TEXT : 1, package : com.skb.tv\n\n"
    },
    {
      "time": 1690881403.146553,
      "raw": " [ 08-01 18:16:44.767  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown keyCode = 82, KeyIndex = 75, KeySets().length = 10, isWebInputType = false, isEditable = false, isTypeNull = true, currentKeyMode = 4, isSearchMode = false, isInputViewShown = false, isAllowApp = false\n\n"
    },
    {
      "time": 1690881403.146588,
      "raw": " [ 08-01 18:16:44.767  4186: 4186 D/BTV_IMEService ]\nime:onKeyDown 00000 keyCode = 82\n\n"
    },
    {
      "time": 1690881403.146601,
      "raw": " [ 08-01 18:16:44.767  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown 00-11 keyCode = 82, getVisibility : 4\n\n"
    },
    {
      "time": 1690881403.146615,
      "raw": " [ 08-01 18:16:44.767  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown 00-11 end ### 6 keyCode = 82\n\n"
    },
    {
      "time": 1690881403.146628,
      "raw": " [ 08-01 18:16:44.768  4531: 4531 I/MainActivity ]\ndispatchKeyEvent() called. (0, 82) | findFocus : org.xwalk.core.internal.XWalkContentView$XWalkContentViewApi23{c612d7b VFE...C.. .F...... 0,0-1920,1080}\n\n"
    },
    {
      "time": 1690881403.14664,
      "raw": " [ 08-01 18:16:44.768  4531: 4531 I/BtvKeyEvent[6]-2023.03.17 ]\ncheckBtvKeyCode outKeyCode : 82, name : 82\n\n"
    },
    {
      "time": 1690881403.146652,
      "raw": " [ 08-01 18:16:44.768  4531: 4531 I/STBGlobal ]\ngetIsRemoteUpdating() called : false\n\n"
    },
    {
      "time": 1690881403.146663,
      "raw": " [ 08-01 18:16:44.770  4531: 4531 I/BTFManager_SystemManager ]\nBTF|getModelName|112|IN|  DeviceInfo::getModelName start\n\n"
    },
    {
      "time": 1690881403.146675,
      "raw": " [ 08-01 18:16:44.771  4646: 5274 I/BtvService_6.3.08 SystemService ]\nAPK BTF|getModelName|252|IN|  DeviceInfo: try : getModelName\n\n"
    },
    {
      "time": 1690881403.146688,
      "raw": " [ 08-01 18:16:44.772  4646: 5274 I/BtvService_6.3.08 SystemService ]\nAPK BTF|getModelName|262|OUT|  DeviceInfo: result : getModelName : BFX-UH200\n\n"
    },
    {
      "time": 1690881403.146699,
      "raw": " [ 08-01 18:16:44.773  4531: 4531 I/BTFManager_NetworkManager ]\nBTF|getNetworkInfo|72|IN|  Ethernet::getNetworkInfo start\n\n"
    },
    {
      "time": 1690881403.155641,
      "raw": " [ 08-01 18:16:44.773  4646: 5274 I/BtvService_6.3.08 NetworkService ]\nAPK BTF|getNetworkInfo|166|IN|  Ethernet: try : getNetworkInfo\n\n"
    },
    {
      "time": 1690881403.155669,
      "raw": " [ 08-01 18:16:44.773  4646: 5274 I/BtvService_6.3.08 NetworkService ]\nAPK BTF|getNetworkInfo|169|OUT|  Ethernet: result : getNetworkInfo : type = dhcp, ip = 192.168.30.25, gateway = 192.168.30.1, subnet = 255.255.255.0, dns1 = 211.44.250.88, dns2 = 121.125.25.110\n\n"
    },
    {
      "time": 1690881403.155683,
      "raw": " [ 08-01 18:16:44.774  4531: 4531 D/ProfileManager ]\ngetActiveProfileId loadOption: BOTH\n\n"
    },
    {
      "time": 1690881403.155696,
      "raw": " [ 08-01 18:16:44.774  4531: 4531 I/STBAPIManager ]\ngetCacheData key: PROFILE_ID\n\n"
    },
    {
      "time": 1690881403.155708,
      "raw": " [ 08-01 18:16:44.774  4531: 4531 D/ProfileManager ]\ngetProfileId: 709c85c0-84c9-4773-8da7-8424854ca413\n\n"
    },
    {
      "time": 1690881403.15572,
      "raw": " [ 08-01 18:16:44.774  4531: 4531 D/ProfileManager ]\ngetProfileIdForLog profileId: 709c85c0-84c9-4773-8da7-8424854ca413\n\n"
    },
    {
      "time": 1690881403.155732,
      "raw": " [ 08-01 18:16:44.774  4531: 4531 D/ProfileManager ]\ngetProfileItem profileId: 709c85c0-84c9-4773-8da7-8424854ca413\n\n"
    },
    {
      "time": 1690881403.155744,
      "raw": " [ 08-01 18:16:44.774  4531: 4531 D/HiddenMenu ]\nkeyType=MENU\n\n"
    },
    {
      "time": 1690881403.155763,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881403.155775,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent keyCode : 82, scanCode : 0, keyAction : 0\n\n"
    },
    {
      "time": 1690881403.155787,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881403.155798,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 D/STBGlobal ]\ngetIsAvailableRedKey mAvailableRedKey  : false\n\n"
    },
    {
      "time": 1690881403.15581,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent getIsAvailableDCA: true, getIsAvailableRedKey: false\n\n"
    },
    {
      "time": 1690881403.155822,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881403.155834,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent keyType: MENU\n\n"
    },
    {
      "time": 1690881403.155846,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 I/MainActivity ]\nonKeyDown() called\n\n"
    },
    {
      "time": 1690881403.155858,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 D/KeyEventManager ]\nonKeyDown : 82\n\n"
    },
    {
      "time": 1690881403.15587,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 D/KeyEventManager ]\nonKeyDown : MENU\n\n"
    },
    {
      "time": 1690881403.155882,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 D/KeyEventManager ]\nprocessKeyHandle() notifyObservers call\n\n"
    },
    {
      "time": 1690881403.155894,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 D/KeyEventObservable ]\nnotifyObservers() MENU  KEY_SINGLE_DOWN\n\n"
    },
    {
      "time": 1690881403.155905,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 I/G2TvFragment ]\nonKeyEvent\n\n"
    },
    {
      "time": 1690881403.155917,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 I/G2TvFragment ]\nonKeyEvent keyEventType : MENU, keyEventAction : KEY_SINGLE_DOWN, isAlreadyProcess : false\n\n"
    },
    {
      "time": 1690881403.155929,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 D/InsideUiManager ]\nisShowInside(), isResult : false\n\n"
    },
    {
      "time": 1690881403.155941,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 I/G2TvFragment ]\nonKeyEvent fragment is G2TvFragment\n\n"
    },
    {
      "time": 1690881403.155953,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 D/STBAPIManager ]\ngetKidsZoneEntry called\n\n"
    },
    {
      "time": 1690881403.155964,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 I/KidszoneManager ]\ngetKidszone(), isProperty : false, Value : 0\n\n"
    },
    {
      "time": 1690881403.155976,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 D/KidszoneManager ]\nprocessExitKidszone | true | false | com.skb.google.tv.bundle.CommandBundle@4b8e6ba\n\n"
    },
    {
      "time": 1690881403.155988,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 D/UIControlManager ]\nprocessBundle() commandBundleType : KEY_MENU,G2TvFragment{235c2ec} (541c4276-26b9-4ed8-b2be-1fc6b7ca2fe2 id=0x7f080668)\n\n"
    },
    {
      "time": 1690881403.156002,
      "raw": " [ 08-01 18:16:44.775  4531: 4531 I/PlayBarConst ]\nneedShowVodKeyLockPopup(), mediaType is not VOD\n\n"
    },
    {
      "time": 1690881403.156016,
      "raw": " [ 08-01 18:16:44.776  4531: 5524 D/NewMenuNaviSendManager ]\nprocessEvent() log : {\"action_body\":{},\"action_id\":\"rcu_event\",\"app_build_version\":\"22558\",\"client_ip\":\"192.168.30.25\",\"contents_body\":{},\"device_base_time\":\"20230801181644.768\",\"device_model\":\"BFX-UH200\",\"edid\":{},\"log_type\":\"live\",\"manufacturer\":\"Foxconn\",\"member\":{\"profile_type\":\"btv\",\"profile_id\":\"709c85c0-84c9-4773-8da7-8424854ca413\",\"nickname\":\"우리집 Btv\"},\"menu_id\":\"\",\"os_name\":\"Android\",\"os_version\":\"10\",\"page_id\":\"/rcu_event\",\"page_path\":\"||rcu_event\",\"page_type\":\"native\",\"pcid\":\"20230427151959325379116\",\"poc_type\":\"stb_app\",\"race\":{},\"remote_control\":{\"battery\":\"low\",\"description\":\"\",\"function\":\"\",\"mac\":\"\",\"model\":\"\",\"rcu_key\":\"menu_all\",\"rcu_key_type\":\"\",\"status\":\"\",\"version\":\"\"},\"service_name\":\"btv\",\"session_id\":\"2023042715195932537911630260\",\"stb_fw_version\":\"17.536.2-0000\",\"stb_id\":\"B2BCE5E3-1374-11EB-B041-09B554E49A17\",\"stb_mac\":\"40:23:43:af:99:a4\",\"url\":\"\",\"vod_watch_type\":\"\",\"web_page_version\":\"5.3.6.005\"}\n\n"
    },
    {
      "time": 1690881403.156029,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/FragmentControl ]\nclearFragmentForSaveType() called. before LIST [G2TvFragment{235c2ec} (541c4276-26b9-4ed8-b2be-1fc6b7ca2fe2 id=0x7f080668)]\n\n"
    },
    {
      "time": 1690881403.156041,
      "raw": " [ 08-01 18:16:44.776  4531: 5524 D/NewMenuNaviSendManager ]\nprocessEvent() timer alive : true\n\n"
    },
    {
      "time": 1690881403.156054,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/FragmentControl ]\nclearFragmentForSaveType() remove size of fragmentList : 0\n\n"
    },
    {
      "time": 1690881403.156066,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/FragmentControl ]\ncorrectionContainer() BEFORE [0][8]\n\n"
    },
    {
      "time": 1690881403.156078,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/FragmentControl ]\ncorrectionContainer() isShowFragment : false currentFragment : G2TvFragment{235c2ec} (541c4276-26b9-4ed8-b2be-1fc6b7ca2fe2 id=0x7f080668)\n\n"
    },
    {
      "time": 1690881403.15609,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/G2TvFragment ]\nisFragmentHidden() isFragmentHidden : false\n\n"
    },
    {
      "time": 1690881403.156101,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/FragmentControl ]\nisUIVisibility() baseFragment : G2TvFragment{235c2ec} (541c4276-26b9-4ed8-b2be-1fc6b7ca2fe2 id=0x7f080668)\n\n"
    },
    {
      "time": 1690881403.156113,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/G2TvFragment ]\nisFragmentHidden() isFragmentHidden : false\n\n"
    },
    {
      "time": 1690881403.156125,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/FragmentControl ]\nisUIVisibility() G2TvFragment is VISIBLE ? true\n\n"
    },
    {
      "time": 1690881403.156137,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/FragmentControl ]\nisUIVisibility() isHidden : false\n\n"
    },
    {
      "time": 1690881403.156149,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/FragmentControl ]\nisUIVisibility() isUIVisibility : true\n\n"
    },
    {
      "time": 1690881403.15616,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/FragmentControl ]\nplayerViewFocusLock() isFocusLock : true\n\n"
    },
    {
      "time": 1690881403.156172,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/FragmentControl ]\ncorrectionContainer() AFTER [0][8]\n\n"
    },
    {
      "time": 1690881403.156184,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/FragmentControl ]\nclearFragmentForSaveType() after LIST [G2TvFragment{235c2ec} (541c4276-26b9-4ed8-b2be-1fc6b7ca2fe2 id=0x7f080668)]\n\n"
    },
    {
      "time": 1690881403.156196,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/SendInterfaceManager ]\nSendInterfaceManager getInstance\n\n"
    },
    {
      "time": 1690881403.156207,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/G2TvFragment ]\nisFragmentHidden() isFragmentHidden : false\n\n"
    },
    {
      "time": 1690881403.156219,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/SendInterfaceManager ]\nsendMenuHotKeyNavigationWeb menuId : NM1000018142/NM1000020100, keyName : allMenu, forwardPopup : false, disableToggle : false\n\n"
    },
    {
      "time": 1690881403.156231,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/InterfaceInfoManager ]\ngetMenuHotKeyNavigationWeb\n\n"
    },
    {
      "time": 1690881403.156243,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/SendCommon ]\ngetSendJsonData\n\n"
    },
    {
      "time": 1690881403.156255,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/SendCommon ]\ngetSendJsonData mCommonObj : {\"TYPE\":\"request\",\"COMMAND\":\"MenuHotKeyNavigationWeb\",\"CONTENTS\":\"\",\"DATA\":{\"menuId\":\"NM1000018142\\/NM1000020100\",\"keyName\":\"allMenu\",\"forwardPopup\":\"N\"}}\n\n"
    },
    {
      "time": 1690881403.156267,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/STBGlobal ]\nisVirtualVodChannel() : false\n\n"
    },
    {
      "time": 1690881403.156279,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/G2TvFragment ]\nisFragmentHidden() isFragmentHidden : false\n\n"
    },
    {
      "time": 1690881403.156291,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/UIControlManager ]\nprocessBundle() commandBundleType : SEND_JSON_DATA,G2TvFragment{235c2ec} (541c4276-26b9-4ed8-b2be-1fc6b7ca2fe2 id=0x7f080668)\n\n"
    },
    {
      "time": 1690881403.156303,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/G2TvFragment ]\nonReceiveBundle\n\n"
    },
    {
      "time": 1690881403.156314,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/G2TvFragment ]\nprocessCommandBundle\n\n"
    },
    {
      "time": 1690881403.156326,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/G2TvFragment ]\nprocessCommandBundle COMMAND_CODE_NAVIGATE_WEB_MENU mSendStbInfo : true\n\n"
    },
    {
      "time": 1690881403.156338,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/G2TvFragment ]\nisFragmentHidden() isFragmentHidden : false\n\n"
    },
    {
      "time": 1690881403.156349,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/G2TvFragment ]\nsendJsonData\n\n"
    },
    {
      "time": 1690881403.159035,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/G2TvFragment ]\nsendJsonData script STB.receiveMessageFromNative({\"TYPE\":\"request\",\"COMMAND\":\"MenuHotKeyNavigationWeb\",\"CONTENTS\":\"\",\"DATA\":{\"menuId\":\"NM1000018142\\/NM1000020100\",\"keyName\":\"allMenu\",\"forwardPopup\":\"N\"}});\n\n"
    },
    {
      "time": 1690881403.159055,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 I/G2TvFragment ]\nprocessCommandBundle ignoreNotify : false\n\n"
    },
    {
      "time": 1690881403.15907,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/KeyEventObservable ]\nnotifyObservers() isAlreadyProcess is true\n\n"
    },
    {
      "time": 1690881403.159081,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/KeyEventManager ]\nprocessKeyHandle() notifyObservers call\n\n"
    },
    {
      "time": 1690881403.159095,
      "raw": " [ 08-01 18:16:44.776  4531: 4531 D/KeyEventObservable ]\nnotifyObservers() MENU  KEY_DOWN\n\n"
    },
    {
      "time": 1690881403.159107,
      "raw": " [ 08-01 18:16:44.777  4531: 4531 D/KeyEventObservable ]\nnotifyObservers() 4  28\n\n"
    },
    {
      "time": 1690881403.159119,
      "raw": " [ 08-01 18:16:44.778  3820:30268 D/WindowManager ]\ninterceptKeyTq keycode=82 interactive=true keyguardActive=false policyFlags=2b000000\n\n"
    },
    {
      "time": 1690881403.159131,
      "raw": " [ 08-01 18:16:44.778  3820: 3907 I/WindowManager ]\ninterceptKeyTi keyCode=82 down=false repeatCount=0 keyguardOn=false canceled=false policyFlags=1795162112 mDeviceId=-1 mSource=0 mScanCode=0 mCharacters=null\n\n"
    },
    {
      "time": 1690881403.159143,
      "raw": " [ 08-01 18:16:44.778  3820: 3907 D/WindowManager ]\ninterceptSkbFuctionKeyBeforeDispatching keycode = 82\n\n"
    },
    {
      "time": 1690881403.159155,
      "raw": " [ 08-01 18:16:44.778  3820: 3907 D/WindowManager ]\nkeycode : 82 - processed. by skb function key\n\n"
    },
    {
      "time": 1690881403.15917,
      "raw": " [ 08-01 18:16:44.778  3820: 3907 W/GlobalKeyManager ]\nhandleGlobalKey keyCode : 82 componentnull\n\n"
    },
    {
      "time": 1690881403.159182,
      "raw": " [ 08-01 18:16:44.779  4531: 4531 I/chromium ]\n[INFO:CONSOLE(1)] \"Uncaught ReferenceError: STB is not defined\", source:  (1)\n\n\n"
    },
    {
      "time": 1690881403.159194,
      "raw": " [ 08-01 18:16:44.779  4186: 4186 I/BTV_IMEService ]\nonKeyUp(), start keyCode = 82, BUILD_DATE : 2023.02.20\n\n"
    },
    {
      "time": 1690881403.159206,
      "raw": " [ 08-01 18:16:44.779  4186: 4186 I/BTV_IMEService ]\nonKeyUp(), end  ## 2 keyCode = 82, result : false\n\n"
    },
    {
      "time": 1690881403.159219,
      "raw": " [ 08-01 18:16:44.779  4646: 4646 I/BtvService_6.3.08 PeripheralService ]\nAPK BTF|onReceive|54| LEDControl:onReceive : com.skb.intent.KEY_LED_BLINK\n\n"
    },
    {
      "time": 1690881403.15923,
      "raw": " [ 08-01 18:16:44.779  4531: 4531 I/MainActivity ]\ndispatchKeyEvent() called. (1, 82) | findFocus : org.xwalk.core.internal.XWalkContentView$XWalkContentViewApi23{c612d7b VFE...C.. .F...... 0,0-1920,1080}\n\n"
    },
    {
      "time": 1690881403.159242,
      "raw": " [ 08-01 18:16:44.779  4531: 4531 I/BtvKeyEvent[6]-2023.03.17 ]\ncheckBtvKeyCode outKeyCode : 82, name : 82\n\n"
    },
    {
      "time": 1690881403.159254,
      "raw": " [ 08-01 18:16:44.779  4531: 4531 I/STBGlobal ]\ngetIsRemoteUpdating() called : false\n\n"
    },
    {
      "time": 1690881403.159266,
      "raw": " [ 08-01 18:16:44.780  4646: 4646 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState index: 3, state: 2, StateQ.size(): 0, BQ.remainingCapa(): 10\n\n"
    },
    {
      "time": 1690881403.159278,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881403.15929,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent keyCode : 82, scanCode : 0, keyAction : 1\n\n"
    },
    {
      "time": 1690881403.159303,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881403.159315,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 D/STBGlobal ]\ngetIsAvailableRedKey mAvailableRedKey  : false\n\n"
    },
    {
      "time": 1690881403.159327,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent getIsAvailableDCA: true, getIsAvailableRedKey: false\n\n"
    },
    {
      "time": 1690881403.159338,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881403.15935,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent keyType: MENU\n\n"
    },
    {
      "time": 1690881403.159362,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 I/MainActivity ]\nonKeyUp() called\n\n"
    },
    {
      "time": 1690881403.159374,
      "raw": " [ 08-01 18:16:44.780  4646: 4763 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState take after  \n\n"
    },
    {
      "time": 1690881403.159386,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 D/KeyEventManager ]\nonKeyUp : 82, isLongKey : false\n\n"
    },
    {
      "time": 1690881403.159398,
      "raw": " [ 08-01 18:16:44.780  4646: 4763 D/BTFSerJni[6][22.06.08] ]\ntvcoreJni_frontPanelSetLedState start\n\n"
    },
    {
      "time": 1690881403.15941,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 D/KeyEventManager ]\nonKeyUp : MENU\n\n"
    },
    {
      "time": 1690881403.159424,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 D/KeyEventManager ]\nprocessKeyHandle() notifyObservers call\n\n"
    },
    {
      "time": 1690881403.159436,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 D/KeyEventObservable ]\nnotifyObservers() MENU  KEY_UP\n\n"
    },
    {
      "time": 1690881403.159451,
      "raw": " [ 08-01 18:16:44.780  4531: 4531 D/KeyEventObservable ]\nnotifyObservers() 4  28\n\n"
    },
    {
      "time": 1690881403.159463,
      "raw": " [ 08-01 18:16:44.781 15093:15093 D/AndroidRuntime ]\nShutting down VM\n\n\n"
    },
    {
      "time": 1690881403.159474,
      "raw": " [ 08-01 18:16:44.783  2790: 2790 I/TVService-23.01.26 ]\n[TVService::frontPanelSetLedState] index(3) state(2).\n\n"
    },
    {
      "time": 1690881403.159487,
      "raw": " [ 08-01 18:16:44.783  2790: 2790 I/FrontPanelManager ]\n[frontPanelSetLedState] called index(3) state(2)\n\n"
    },
    {
      "time": 1690881403.159502,
      "raw": " [ 08-01 18:16:44.783  2790: 2790 W/btvSocHalService-JNI ]\nbtvSocHalService_SetLedState::991 : in \n\n"
    },
    {
      "time": 1690881403.159514,
      "raw": " [ 08-01 18:16:44.783  3564: 5656 D/DEVICE   ]\nBTF|DEVICE_SetLedState|85|IN| device:ee910218, led_id:3, state:2\n\n\n"
    },
    {
      "time": 1690881403.258156,
      "raw": " [ 08-01 18:16:44.783  3564: 5656 D/DEVICE   ]\n++DEVICE_SetLedState led_id(3), state(2) \n\n"
    },
    {
      "time": 1690881403.260963,
      "raw": " [ 08-01 18:16:44.783  3564: 5656 D/hal_frontpanel ]\nhal_frontpanel:HAL_FrontPanelSetLedState v102(3, 2)\n\n"
    },
    {
      "time": 1690881403.260999,
      "raw": " [ 08-01 18:16:44.885  3564: 5656 D/DEVICE   ]\nBTF|DEVICE_SetLedState|111|OUT| \n\n\n"
    },
    {
      "time": 1690881403.261013,
      "raw": " [ 08-01 18:16:44.885  2790: 2790 W/btvSocHalService-JNI ]\nbtvSocHalService_SetLedState::994 : out, opStatus:0 \n\n"
    },
    {
      "time": 1690881403.380507,
      "raw": " [ 08-01 18:16:44.885  4646: 4763 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState after jni, index: 3, status: 2, result: true\n\n"
    },
    {
      "time": 1690881403.383224,
      "raw": " [ 08-01 18:16:44.885  4646: 4763 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState take before ===============================================\n\n"
    },
    {
      "time": 1690881403.49455,
      "raw": " [ 08-01 18:16:45.008  2790:13944 D/BOXKEY-STDVB ]\n[DEVICE 0] ++ remain buffer size : 27636\n\n"
    },
    {
      "time": 1690881403.494647,
      "raw": " [ 08-01 18:16:45.010  3564:13967 I/HalAudioOutput ]\noutputRate:48030(1.00)\n\n"
    },
    {
      "time": 1690881403.494668,
      "raw": " [ 08-01 18:16:45.122  3587:15108 I/adbd     ]\nhost-72: read thread spawning\n\n"
    },
    {
      "time": 1690881403.494686,
      "raw": " [ 08-01 18:16:45.122  3587:15108 I/adbd     ]\nhost-72: read failed: Success\n\n"
    },
    {
      "time": 1690881403.494704,
      "raw": " [ 08-01 18:16:45.122  3587:15108 I/adbd     ]\nhost-72: connection terminated: read failed\n\n"
    },
    {
      "time": 1690881403.494722,
      "raw": " [ 08-01 18:16:45.122  3587: 3587 I/adbd     ]\nhost-72: already offline\n\n"
    },
    {
      "time": 1690881403.494739,
      "raw": " [ 08-01 18:16:45.122  3587: 3587 I/adbd     ]\ndestroying transport host-72\n\n"
    },
    {
      "time": 1690881403.494756,
      "raw": " [ 08-01 18:16:45.122  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-72): stopping\n\n"
    },
    {
      "time": 1690881403.497133,
      "raw": " [ 08-01 18:16:45.123  3587:15109 I/adbd     ]\nhost-72: write thread spawning\n\n"
    },
    {
      "time": 1690881403.49718,
      "raw": " [ 08-01 18:16:45.123  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-72): stopped\n\n"
    },
    {
      "time": 1690881403.57858,
      "raw": " [ 08-01 18:16:45.123  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-72): destructing\n\n"
    },
    {
      "time": 1690881403.617669,
      "raw": " [ 08-01 18:16:45.123  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-72): already stopped\n\n"
    },
    {
      "time": 1690881403.718202,
      "raw": " [ 08-01 18:16:45.206  3564:13953 I/MiniAmVideoDec_0 ]\nvbuf:936026/2097152, rp:0x5b94f22, latency:1251.24ms\n\n"
    },
    {
      "time": 1690881403.72014,
      "raw": " [ 08-01 18:16:45.245  3564:13946 I/LivePlayer_0 ]\nSEAN onCheckVoiceAssistant(mString: nugu_playback=off)\n\n"
    },
{
      "time": 1690881417.125823,
      "raw": " [ 08-01 18:16:58.586  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-72): already stopped\n\n"
    },
    {
      "time": 1690881417.125871,
      "raw": " [ 08-01 18:16:58.615  3564:13947 W/RendererPolicyBase_0 ]\nvideo render: 59.94 fps, drop: 0.00 fps\n\n"
    },
    {
      "time": 1690881417.135008,
      "raw": " [ 08-01 18:16:58.749  3499: 3499 W/ATVRemoteAudioH ]\ntype=1400 audit(0.0:3675860): avc: denied { call } for scontext=u:r:hal_audio_amlogic:s0 tcontext=u:r:rc_server:s0 tclass=binder permissive=0\n\n"
    },
    {
      "time": 1690881417.380033,
      "raw": " [ 08-01 18:16:58.752  3499: 3745 W/ServiceManagement ]\ngetService: unable to call into hwbinder service for vendor.amlogic.hardware.remotecontrol@1.0::IRemoteControl/default.\n\n"
    },
    {
      "time": 1690881417.487746,
      "raw": " [ 08-01 18:16:58.762  3564:13946 I/LivePlayer_0 ]\nSEAN onCheckVoiceAssistant(mString: nugu_playback=off)\n\n"
    },
    {
      "time": 1690881417.492794,
      "raw": " [ 08-01 18:16:59.006  2790:13944 D/BOXKEY-STDVB ]\n[DEVICE 0] ++ remain buffer size : 28952\n\n"
    },
    {
      "time": 1690881417.498758,
      "raw": " [ 08-01 18:16:59.115  3564:13967 I/HalAudioOutput ]\noutputRate:48003(1.00)\n\n"
    },
    {
      "time": 1690881417.507843,
      "raw": " [ 08-01 18:16:59.118  4490: 4490 D/MDNSService ]\nMDNSMsgHandler() AM_EVENT_CHECK_NETWORK_CONFIG. isConnected : true\n\n"
    },
    {
      "time": 1690881417.509674,
      "raw": " [ 08-01 18:16:59.126 15298:15298 D/AndroidRuntime ]\n>>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<\n\n\n"
    },
    {
      "time": 1690881417.514578,
      "raw": " [ 08-01 18:16:59.135 15298:15298 I/AndroidRuntime ]\nUsing default boot image\n\n"
    },
    {
      "time": 1690881417.517064,
      "raw": " [ 08-01 18:16:59.135 15298:15298 I/AndroidRuntime ]\nLeaving lock profiling enabled\n\n"
    },
    {
      "time": 1690881417.586898,
      "raw": " [ 08-01 18:16:59.142 15298:15298 W/app_process ]\nCould not reserve sentinel fault page\n\n"
    },
    {
      "time": 1690881417.635151,
      "raw": " [ 08-01 18:16:59.142 15298:15298 I/app_process ]\nCore platform API reporting enabled, enforcing=false\n\n"
    },
    {
      "time": 1690881417.713855,
      "raw": " [ 08-01 18:16:59.214  3564:13953 I/MiniAmVideoDec_0 ]\nvbuf:1017096/2097152, rp:0x6bc7479, latency:1234.57ms\n\n"
    },
    {
      "time": 1690881417.719446,
      "raw": " [ 08-01 18:16:59.263  3564:13946 I/LivePlayer_0 ]\nSEAN onCheckVoiceAssistant(mString: nugu_playback=off)\n\n"
    },
    {
      "time": 1690881417.723346,
      "raw": " [ 08-01 18:16:59.341 15298:15298 D/ICU      ]\nTime zone APEX file found: /apex/com.android.tzdata/etc/icu/icu_tzdata.dat\n\n"
    },
    {
      "time": 1690881417.733762,
      "raw": " [ 08-01 18:16:59.347  2790:13937 E/libc     ]\nAccess denied finding property \"skb.audio.output\"\n\n"
    },
    {
      "time": 1690881417.736488,
      "raw": " [ 08-01 18:16:59.345  2790: 2790 W/btvservice@1.0- ]\ntype=1400 audit(0.0:3675861): avc: denied { read } for name=\"u:object_r:default_prop:s0\" dev=\"tmpfs\" ino=189 scontext=u:r:btvservice_hal:s0 tcontext=u:object_r:default_prop:s0 tclass=file permissive=0\n\n"
    },
    {
      "time": 1690881417.778256,
      "raw": " [ 08-01 18:16:59.361 15298:15298 W/app_process ]\nUsing default instruction set features for ARM CPU variant (cortex-a9) using conservative defaults\n\n"
    },
    {
      "time": 1690881417.791635,
      "raw": " [ 08-01 18:16:59.364 15298:15298 I/app_process ]\nThe ClassLoaderContext is a special shared library.\n\n"
    },
    {
      "time": 1690881417.794344,
      "raw": " [ 08-01 18:16:59.406 15298:15298 W/app_process ]\nJNI RegisterNativeMethods: attempt to register 0 native methods for android.media.AudioAttributes\n\n"
    },
    {
      "time": 1690881417.797284,
      "raw": " [ 08-01 18:16:59.419 15298:15298 D/AndroidRuntime ]\nCalling main entry com.android.commands.input.Input\n\n"
    },
    {
      "time": 1690881417.79986,
      "raw": " [ 08-01 18:16:59.422 15298:15298 V/KeyEvent ]\n  keyCodeFromString ##2 keyCode: 92, LAST_KEYCODE : 454\n\n"
    },
    {
      "time": 1690881417.799892,
      "raw": " [ 08-01 18:16:59.424  3820:18159 D/WindowManager ]\ninterceptKeyTq keycode=92 interactive=true keyguardActive=false policyFlags=2b000000\n\n"
    },
    {
      "time": 1690881417.804137,
      "raw": " [ 08-01 18:16:59.425  3820: 3907 I/WindowManager ]\ninterceptKeyTi keyCode=92 down=true repeatCount=0 keyguardOn=false canceled=false policyFlags=1795162112 mDeviceId=-1 mSource=0 mScanCode=0 mCharacters=null\n\n"
    },
    {
      "time": 1690881417.809646,
      "raw": " [ 08-01 18:16:59.426  3820: 3907 D/WindowManager ]\ninterceptKeyTi strDate 2023-08-01 18:16\n\n"
    },
    {
      "time": 1690881417.811937,
      "raw": " [ 08-01 18:16:59.427  3820: 3907 D/WindowManager ]\ninterceptSkbFuctionKeyBeforeDispatching keycode = 92\n\n"
    },
    {
      "time": 1690881417.811971,
      "raw": " [ 08-01 18:16:59.427  3820: 3907 D/WindowManager ]\nkeycode : 92 - processed. by skb function key\n\n"
    },
    {
      "time": 1690881417.811987,
      "raw": " [ 08-01 18:16:59.427  3820: 3907 W/GlobalKeyManager ]\nhandleGlobalKey keyCode : 92 componentnull\n\n"
    },
    {
      "time": 1690881417.812003,
      "raw": " [ 08-01 18:16:59.428  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown start keyCode = 92, packageName: com.skb.tv\n\n"
    },
    {
      "time": 1690881417.81202,
      "raw": " [ 08-01 18:16:59.428  4186: 4186 W/BTV_IME-InputAttributes ]\nisAllowApp mInputType :0, TYPE_CLASS_TEXT : 1, package : com.skb.tv\n\n"
    },
    {
      "time": 1690881417.81205,
      "raw": " [ 08-01 18:16:59.428  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown keyCode = 92, KeyIndex = 85, KeySets().length = 10, isWebInputType = false, isEditable = false, isTypeNull = true, currentKeyMode = 4, isSearchMode = false, isInputViewShown = false, isAllowApp = false\n\n"
    },
    {
      "time": 1690881417.812065,
      "raw": " [ 08-01 18:16:59.428  4186: 4186 D/BTV_IMEService ]\nime:onKeyDown 00000 keyCode = 92\n\n"
    },
    {
      "time": 1690881417.812084,
      "raw": " [ 08-01 18:16:59.428  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown 00-11 keyCode = 92, getVisibility : 4\n\n"
    },
    {
      "time": 1690881417.812102,
      "raw": " [ 08-01 18:16:59.428  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown 00-11 end ### 6 keyCode = 92\n\n"
    },
    {
      "time": 1690881417.812118,
      "raw": " [ 08-01 18:16:59.429  4531: 4531 I/MainActivity ]\ndispatchKeyEvent() called. (0, 92) | findFocus : org.xwalk.core.internal.XWalkContentView$XWalkContentViewApi23{c612d7b VFE...C.. .F...... 0,0-1920,1080}\n\n"
    },
    {
      "time": 1690881417.812135,
      "raw": " [ 08-01 18:16:59.429  4531: 4531 I/BtvKeyEvent[6]-2023.03.17 ]\ncheckBtvKeyCode outKeyCode : 92, name : 92\n\n"
    },
    {
      "time": 1690881417.812152,
      "raw": " [ 08-01 18:16:59.429  4531: 4531 I/STBGlobal ]\ngetIsRemoteUpdating() called : false\n\n"
    },
    {
      "time": 1690881417.812168,
      "raw": " [ 08-01 18:16:59.429  4531: 4531 D/HiddenMenu ]\nkeyType=NONE\n\n"
    },
    {
      "time": 1690881417.812187,
      "raw": " [ 08-01 18:16:59.429  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881417.8122,
      "raw": " [ 08-01 18:16:59.429  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent keyCode : 92, scanCode : 0, keyAction : 0\n\n"
    },
    {
      "time": 1690881417.812217,
      "raw": " [ 08-01 18:16:59.429  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881417.812232,
      "raw": " [ 08-01 18:16:59.429  4531: 4531 D/STBGlobal ]\ngetIsAvailableRedKey mAvailableRedKey  : false\n\n"
    },
    {
      "time": 1690881417.812243,
      "raw": " [ 08-01 18:16:59.429  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent getIsAvailableDCA: true, getIsAvailableRedKey: false\n\n"
    },
    {
      "time": 1690881417.812262,
      "raw": " [ 08-01 18:16:59.429  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881417.812279,
      "raw": " [ 08-01 18:16:59.429  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881417.812296,
      "raw": " [ 08-01 18:16:59.431  4531: 4531 I/G2TvFragment ]\nonUnhandledKeyEvent keyCode : 92, scanCode : 0, keyAction : 0\n\n"
    },
    {
      "time": 1690881417.812308,
      "raw": " [ 08-01 18:16:59.431  4531: 4531 D/MainActivity - NextTvFragment ]\nmakingKeyEvent called type: null\n\n"
    },
    {
      "time": 1690881417.812323,
      "raw": " [ 08-01 18:16:59.431  4531: 4531 I/G2TvFragment ]\nonUnhandledKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881417.81234,
      "raw": " [ 08-01 18:16:59.432  3820:18159 D/WindowManager ]\ninterceptKeyTq keycode=92 interactive=true keyguardActive=false policyFlags=2b000000\n\n"
    },
    {
      "time": 1690881417.812352,
      "raw": " [ 08-01 18:16:59.432  3820: 3907 I/WindowManager ]\ninterceptKeyTi keyCode=92 down=false repeatCount=0 keyguardOn=false canceled=false policyFlags=1795162112 mDeviceId=-1 mSource=0 mScanCode=0 mCharacters=null\n\n"
    },
    {
      "time": 1690881417.812364,
      "raw": " [ 08-01 18:16:59.432  3820: 3907 D/WindowManager ]\ninterceptSkbFuctionKeyBeforeDispatching keycode = 92\n\n"
    },
    {
      "time": 1690881417.812382,
      "raw": " [ 08-01 18:16:59.433  3820: 3907 D/WindowManager ]\nkeycode : 92 - processed. by skb function key\n\n"
    },
    {
      "time": 1690881417.812396,
      "raw": " [ 08-01 18:16:59.433  3820: 3907 W/GlobalKeyManager ]\nhandleGlobalKey keyCode : 92 componentnull\n\n"
    },
    {
      "time": 1690881417.812409,
      "raw": " [ 08-01 18:16:59.434  4646: 4646 I/BtvService_6.3.08 PeripheralService ]\nAPK BTF|onReceive|54| LEDControl:onReceive : com.skb.intent.KEY_LED_BLINK\n\n"
    },
    {
      "time": 1690881417.812421,
      "raw": " [ 08-01 18:16:59.435  4646: 4646 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState index: 3, state: 2, StateQ.size(): 0, BQ.remainingCapa(): 10\n\n"
    },
    {
      "time": 1690881417.812436,
      "raw": " [ 08-01 18:16:59.435  4646: 4763 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState take after  \n\n"
    },
    {
      "time": 1690881417.812452,
      "raw": " [ 08-01 18:16:59.435  4646: 4763 D/BTFSerJni[6][22.06.08] ]\ntvcoreJni_frontPanelSetLedState start\n\n"
    },
    {
      "time": 1690881417.81247,
      "raw": " [ 08-01 18:16:59.435  2790: 2790 I/TVService-23.01.26 ]\n[TVService::frontPanelSetLedState] index(3) state(2).\n\n"
    },
    {
      "time": 1690881417.812491,
      "raw": " [ 08-01 18:16:59.435  2790: 2790 I/FrontPanelManager ]\n[frontPanelSetLedState] called index(3) state(2)\n\n"
    },
    {
      "time": 1690881417.812507,
      "raw": " [ 08-01 18:16:59.436  2790: 2790 W/btvSocHalService-JNI ]\nbtvSocHalService_SetLedState::991 : in \n\n"
    },
    {
      "time": 1690881417.812524,
      "raw": " [ 08-01 18:16:59.436  4186: 4186 I/BTV_IMEService ]\nonKeyUp(), start keyCode = 92, BUILD_DATE : 2023.02.20\n\n"
    },
    {
      "time": 1690881417.812545,
      "raw": " [ 08-01 18:16:59.436  4186: 4186 I/BTV_IMEService ]\nonKeyUp(), end  ## 2 keyCode = 92, result : false\n\n"
    },
    {
      "time": 1690881417.812564,
      "raw": " [ 08-01 18:16:59.436  3564: 3723 D/DEVICE   ]\nBTF|DEVICE_SetLedState|85|IN| device:ee910218, led_id:3, state:2\n\n\n"
    },
    {
      "time": 1690881417.81258,
      "raw": " [ 08-01 18:16:59.436  3564: 3723 D/DEVICE   ]\n++DEVICE_SetLedState led_id(3), state(2) \n\n"
    },
    {
      "time": 1690881417.812597,
      "raw": " [ 08-01 18:16:59.436  3564: 3723 D/hal_frontpanel ]\nhal_frontpanel:HAL_FrontPanelSetLedState v102(3, 2)\n\n"
    },
    {
      "time": 1690881417.812616,
      "raw": " [ 08-01 18:16:59.436  4531: 4531 I/MainActivity ]\ndispatchKeyEvent() called. (1, 92) | findFocus : org.xwalk.core.internal.XWalkContentView$XWalkContentViewApi23{c612d7b VFE...C.. .F...... 0,0-1920,1080}\n\n"
    },
    {
      "time": 1690881417.812635,
      "raw": " [ 08-01 18:16:59.436  4531: 4531 I/BtvKeyEvent[6]-2023.03.17 ]\ncheckBtvKeyCode outKeyCode : 92, name : 92\n\n"
    },
    {
      "time": 1690881417.814151,
      "raw": " [ 08-01 18:16:59.436  4531: 4531 I/STBGlobal ]\ngetIsRemoteUpdating() called : false\n\n"
    },
    {
      "time": 1690881417.814175,
      "raw": " [ 08-01 18:16:59.436  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881417.814187,
      "raw": " [ 08-01 18:16:59.436  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent keyCode : 92, scanCode : 0, keyAction : 1\n\n"
    },
    {
      "time": 1690881417.814198,
      "raw": " [ 08-01 18:16:59.436  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881417.81421,
      "raw": " [ 08-01 18:16:59.436  4531: 4531 D/STBGlobal ]\ngetIsAvailableRedKey mAvailableRedKey  : false\n\n"
    },
    {
      "time": 1690881417.814222,
      "raw": " [ 08-01 18:16:59.436  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent getIsAvailableDCA: true, getIsAvailableRedKey: false\n\n"
    },
    {
      "time": 1690881417.814234,
      "raw": " [ 08-01 18:16:59.436  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881417.814249,
      "raw": " [ 08-01 18:16:59.436  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881417.81426,
      "raw": " [ 08-01 18:16:59.438 15298:15298 D/AndroidRuntime ]\nShutting down VM\n\n\n"
    },
    {
      "time": 1690881417.814272,
      "raw": " [ 08-01 18:16:59.440  4531: 4531 I/G2TvFragment ]\nonUnhandledKeyEvent keyCode : 92, scanCode : 0, keyAction : 1\n\n"
    },
    {
      "time": 1690881417.910809,
      "raw": " [ 08-01 18:16:59.440  4531: 4531 D/MainActivity - NextTvFragment ]\nmakingKeyEvent called type: null\n\n"
    },
    {
      "time": 1690881417.910866,
      "raw": " [ 08-01 18:16:59.440  4531: 4531 I/G2TvFragment ]\nonUnhandledKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881417.910885,
      "raw": " [ 08-01 18:16:59.538  3564: 3723 D/DEVICE   ]\nBTF|DEVICE_SetLedState|111|OUT| \n\n\n"
    },
    {
      "time": 1690881417.910903,
      "raw": " [ 08-01 18:16:59.538  2790: 2790 W/btvSocHalService-JNI ]\nbtvSocHalService_SetLedState::994 : out, opStatus:0 \n\n"
    },
{
      "time": 1690881439.000353,
      "raw": " [ 08-01 18:17:20.605 15589:15589 D/AndroidRuntime ]\nCalling main entry com.android.commands.input.Input\n\n"
    },
    {
      "time": 1690881439.000402,
      "raw": " [ 08-01 18:17:20.613 15589:15589 V/KeyEvent ]\n  keyCodeFromString ##2 keyCode: 19, LAST_KEYCODE : 454\n\n"
    },
    {
      "time": 1690881439.000425,
      "raw": " [ 08-01 18:17:20.616  3820:15257 D/WindowManager ]\ninterceptKeyTq keycode=19 interactive=true keyguardActive=false policyFlags=2b000000\n\n"
    },
    {
      "time": 1690881439.000442,
      "raw": " [ 08-01 18:17:20.618  3820: 3907 I/WindowManager ]\ninterceptKeyTi keyCode=19 down=true repeatCount=0 keyguardOn=false canceled=false policyFlags=1795162112 mDeviceId=-1 mSource=0 mScanCode=0 mCharacters=null\n\n"
    },
    {
      "time": 1690881439.000459,
      "raw": " [ 08-01 18:17:20.618  3820: 3907 D/WindowManager ]\ninterceptKeyTi strDate 2023-08-01 18:17\n\n"
    },
    {
      "time": 1690881439.003061,
      "raw": " [ 08-01 18:17:20.621  3820: 3907 D/WindowManager ]\ninterceptSkbFuctionKeyBeforeDispatching keycode = 19\n\n"
    },
    {
      "time": 1690881439.00685,
      "raw": " [ 08-01 18:17:20.621  3820: 3907 D/WindowManager ]\nkeycode : 19 - processed. by skb function key\n\n"
    },
    {
      "time": 1690881439.010947,
      "raw": " [ 08-01 18:17:20.621  3820: 3907 W/GlobalKeyManager ]\nhandleGlobalKey keyCode : 19 componentnull\n\n"
    },
    {
      "time": 1690881439.01098,
      "raw": " [ 08-01 18:17:20.623  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown start keyCode = 19, packageName: com.skb.tv\n\n"
    },
    {
      "time": 1690881439.010999,
      "raw": " [ 08-01 18:17:20.624  4186: 4186 W/BTV_IME-InputAttributes ]\nisAllowApp mInputType :0, TYPE_CLASS_TEXT : 1, package : com.skb.tv\n\n"
    },
    {
      "time": 1690881439.011018,
      "raw": " [ 08-01 18:17:20.624  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown keyCode = 19, KeyIndex = 12, KeySets().length = 10, isWebInputType = false, isEditable = false, isTypeNull = true, currentKeyMode = 4, isSearchMode = false, isInputViewShown = false, isAllowApp = false\n\n"
    },
    {
      "time": 1690881439.011035,
      "raw": " [ 08-01 18:17:20.624  4186: 4186 D/BTV_IMEService ]\nime:onKeyDown 00000 keyCode = 19\n\n"
    },
    {
      "time": 1690881439.014457,
      "raw": " [ 08-01 18:17:20.624  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown 00-11 keyCode = 19, getVisibility : 4\n\n"
    },
    {
      "time": 1690881439.014495,
      "raw": " [ 08-01 18:17:20.624  4186: 4186 I/BTV_IMEService ]\nime:onKeyDown 00-11 end ### 6 keyCode = 19\n\n"
    },
    {
      "time": 1690881439.014509,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 I/MainActivity ]\ndispatchKeyEvent() called. (0, 19) | findFocus : org.xwalk.core.internal.XWalkContentView$XWalkContentViewApi23{c612d7b VFE...C.. .F...... 0,0-1920,1080}\n\n"
    },
    {
      "time": 1690881439.014522,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 I/BtvKeyEvent[6]-2023.03.17 ]\ncheckBtvKeyCode outKeyCode : 19, name : 19\n\n"
    },
    {
      "time": 1690881439.014534,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 I/STBGlobal ]\ngetIsRemoteUpdating() called : false\n\n"
    },
    {
      "time": 1690881439.014546,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 D/MainActivity ]\nsendAudioScreenDisable | null\n\n"
    },
    {
      "time": 1690881439.017675,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 D/HiddenMenu ]\nkeyType=NONE\n\n"
    },
    {
      "time": 1690881439.017701,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881439.017713,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent keyCode : 19, scanCode : 0, keyAction : 0\n\n"
    },
    {
      "time": 1690881439.017733,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881439.017745,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 D/STBGlobal ]\ngetIsAvailableRedKey mAvailableRedKey  : false\n\n"
    },
    {
      "time": 1690881439.017757,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent getIsAvailableDCA: true, getIsAvailableRedKey: false\n\n"
    },
    {
      "time": 1690881439.017768,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881439.01778,
      "raw": " [ 08-01 18:17:20.628  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881439.017792,
      "raw": " [ 08-01 18:17:20.630  3820:15257 D/WindowManager ]\ninterceptKeyTq keycode=19 interactive=true keyguardActive=false policyFlags=2b000000\n\n"
    },
    {
      "time": 1690881439.017804,
      "raw": " [ 08-01 18:17:20.631  4531: 4531 I/G2TvFragment ]\nonUnhandledKeyEvent keyCode : 19, scanCode : 0, keyAction : 0\n\n"
    },
    {
      "time": 1690881439.017816,
      "raw": " [ 08-01 18:17:20.631  4531: 4531 D/MainActivity - NextTvFragment ]\nmakingKeyEvent called type: null\n\n"
    },
    {
      "time": 1690881439.017828,
      "raw": " [ 08-01 18:17:20.631  4531: 4531 I/G2TvFragment ]\nonUnhandledKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881439.01784,
      "raw": " [ 08-01 18:17:20.632  3820: 3907 I/WindowManager ]\ninterceptKeyTi keyCode=19 down=false repeatCount=0 keyguardOn=false canceled=false policyFlags=1795162112 mDeviceId=-1 mSource=0 mScanCode=0 mCharacters=null\n\n"
    },
    {
      "time": 1690881439.017852,
      "raw": " [ 08-01 18:17:20.632  3820: 3907 D/WindowManager ]\ninterceptSkbFuctionKeyBeforeDispatching keycode = 19\n\n"
    },
    {
      "time": 1690881439.017864,
      "raw": " [ 08-01 18:17:20.632  3820: 3907 D/WindowManager ]\nkeycode : 19 - processed. by skb function key\n\n"
    },
    {
      "time": 1690881439.017875,
      "raw": " [ 08-01 18:17:20.632  3820: 3907 W/GlobalKeyManager ]\nhandleGlobalKey keyCode : 19 componentnull\n\n"
    },
    {
      "time": 1690881439.017887,
      "raw": " [ 08-01 18:17:20.633  4186: 4186 I/BTV_IMEService ]\nonKeyUp(), start keyCode = 19, BUILD_DATE : 2023.02.20\n\n"
    },
    {
      "time": 1690881439.017899,
      "raw": " [ 08-01 18:17:20.633  4186: 4186 I/BTV_IMEService ]\nonKeyUp(), end  ## 2 keyCode = 19, result : false\n\n"
    },
    {
      "time": 1690881439.01791,
      "raw": " [ 08-01 18:17:20.633  4531: 4531 I/MainActivity ]\ndispatchKeyEvent() called. (1, 19) | findFocus : org.xwalk.core.internal.XWalkContentView$XWalkContentViewApi23{c612d7b VFE...C.. .F...... 0,0-1920,1080}\n\n"
    },
    {
      "time": 1690881439.017922,
      "raw": " [ 08-01 18:17:20.634  4531: 4531 I/BtvKeyEvent[6]-2023.03.17 ]\ncheckBtvKeyCode outKeyCode : 19, name : 19\n\n"
    },
    {
      "time": 1690881439.017934,
      "raw": " [ 08-01 18:17:20.634  4531: 4531 I/STBGlobal ]\ngetIsRemoteUpdating() called : false\n\n"
    },
    {
      "time": 1690881439.017945,
      "raw": " [ 08-01 18:17:20.634  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881439.017957,
      "raw": " [ 08-01 18:17:20.634  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent keyCode : 19, scanCode : 0, keyAction : 1\n\n"
    },
    {
      "time": 1690881439.017969,
      "raw": " [ 08-01 18:17:20.634  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881439.01798,
      "raw": " [ 08-01 18:17:20.634  4531: 4531 D/STBGlobal ]\ngetIsAvailableRedKey mAvailableRedKey  : false\n\n"
    },
    {
      "time": 1690881439.017992,
      "raw": " [ 08-01 18:17:20.634  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent getIsAvailableDCA: true, getIsAvailableRedKey: false\n\n"
    },
    {
      "time": 1690881439.018004,
      "raw": " [ 08-01 18:17:20.634  4531: 4531 D/STBGlobal ]\ngetIsAvailableDCA mAvailableDCA  : true\n\n"
    },
    {
      "time": 1690881439.018015,
      "raw": " [ 08-01 18:17:20.634  4531: 4531 I/G2TvFragment ]\nshouldOverrideKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881439.018028,
      "raw": " [ 08-01 18:17:20.634  4646: 4646 I/BtvService_6.3.08 PeripheralService ]\nAPK BTF|onReceive|54| LEDControl:onReceive : com.skb.intent.KEY_LED_BLINK\n\n"
    },
    {
      "time": 1690881439.018047,
      "raw": " [ 08-01 18:17:20.634  4646: 4646 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState index: 3, state: 2, StateQ.size(): 0, BQ.remainingCapa(): 10\n\n"
    },
    {
      "time": 1690881439.01806,
      "raw": " [ 08-01 18:17:20.635  4646: 4763 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState take after  \n\n"
    },
    {
      "time": 1690881439.018072,
      "raw": " [ 08-01 18:17:20.635  4646: 4763 D/BTFSerJni[6][22.06.08] ]\ntvcoreJni_frontPanelSetLedState start\n\n"
    },
    {
      "time": 1690881439.018086,
      "raw": " [ 08-01 18:17:20.636  4531: 4531 I/G2TvFragment ]\nonUnhandledKeyEvent keyCode : 19, scanCode : 0, keyAction : 1\n\n"
    },
    {
      "time": 1690881439.018097,
      "raw": " [ 08-01 18:17:20.636  4531: 4531 D/MainActivity - NextTvFragment ]\nmakingKeyEvent called type: null\n\n"
    },
    {
      "time": 1690881439.018109,
      "raw": " [ 08-01 18:17:20.636  4531: 4531 I/G2TvFragment ]\nonUnhandledKeyEvent mBassKeyCode : false\n\n"
    },
    {
      "time": 1690881439.018121,
      "raw": " [ 08-01 18:17:20.637  2790: 2790 I/TVService-23.01.26 ]\n[TVService::frontPanelSetLedState] index(3) state(2).\n\n"
    },
    {
      "time": 1690881439.018132,
      "raw": " [ 08-01 18:17:20.637  2790: 2790 I/FrontPanelManager ]\n[frontPanelSetLedState] called index(3) state(2)\n\n"
    },
    {
      "time": 1690881439.018147,
      "raw": " [ 08-01 18:17:20.637  2790: 2790 W/btvSocHalService-JNI ]\nbtvSocHalService_SetLedState::991 : in \n\n"
    },
    {
      "time": 1690881439.018159,
      "raw": " [ 08-01 18:17:20.637  3564: 3564 D/DEVICE   ]\nBTF|DEVICE_SetLedState|85|IN| device:ee910218, led_id:3, state:2\n\n\n"
    },
    {
      "time": 1690881439.018171,
      "raw": " [ 08-01 18:17:20.637  3564: 3564 D/DEVICE   ]\n++DEVICE_SetLedState led_id(3), state(2) \n\n"
    },
    {
      "time": 1690881439.018183,
      "raw": " [ 08-01 18:17:20.637  3564: 3564 D/hal_frontpanel ]\nhal_frontpanel:HAL_FrontPanelSetLedState v102(3, 2)\n\n"
    },
    {
      "time": 1690881439.018197,
      "raw": " [ 08-01 18:17:20.638  3564:13947 W/RendererPolicyBase_0 ]\nvideo render: 59.94 fps, drop: 0.00 fps\n\n"
    },
    {
      "time": 1690881439.032507,
      "raw": " [ 08-01 18:17:20.638 15589:15589 D/AndroidRuntime ]\nShutting down VM\n\n\n"
    },
    {
      "time": 1690881439.039045,
      "raw": " [ 08-01 18:17:20.643  4531: 4531 I/ToastUtil ]\nhideLitePopup() called\n\n"
    },
    {
      "time": 1690881439.044862,
      "raw": " [ 08-01 18:17:20.653  3561: 4183 I/[Gralloc] ]\nddebug, free share_fd=100, user_hnd=0xa, ion client=26\n\n\n"
    },
    {
      "time": 1690881439.044905,
      "raw": " [ 08-01 18:17:20.654  4531: 4707 I/[Gralloc] ]\nddebug, free share_fd=270, user_hnd=0xf, ion client=112\n\n\n"
    },
    {
      "time": 1690881439.044928,
      "raw": " [ 08-01 18:17:20.655  4531: 4707 I/[Gralloc] ]\nddebug, free share_fd=251, user_hnd=0xd, ion client=112\n\n\n"
    },
    {
      "time": 1690881439.044945,
      "raw": " [ 08-01 18:17:20.657  4531: 4707 I/[Gralloc] ]\nddebug, free share_fd=262, user_hnd=0xe, ion client=112\n\n\n"
    },
    {
      "time": 1690881439.044967,
      "raw": " [ 08-01 18:17:20.657  3561: 4183 E/BufferQueueProducer ]\n[#0] disconnect: not connected (req=1)\n\n"
    },
    {
      "time": 1690881439.048746,
      "raw": " [ 08-01 18:17:20.657  3561: 3561 I/[Gralloc] ]\nddebug, free share_fd=84, user_hnd=0x8, ion client=26\n\n\n"
    },
    {
      "time": 1690881439.048791,
      "raw": " [ 08-01 18:17:20.657  4531: 4707 W/libEGL   ]\nEGLNativeWindowType 0xbd1b0548 disconnect failed\n\n"
    },
    {
      "time": 1690881439.051472,
      "raw": " [ 08-01 18:17:20.675  4531: 4531 D/ToastUtil ]\nAlphaAnimator End\n\n"
    },
    {
      "time": 1690881439.051507,
      "raw": " [ 08-01 18:17:20.675  3511: 3702 I/[Gralloc] ]\nddebug, free share_fd=58, user_hnd=0x6, ion client=31\n\n\n"
    },
    {
      "time": 1690881439.051523,
      "raw": " [ 08-01 18:17:20.676  3511: 3702 I/[Gralloc] ]\nddebug, free share_fd=68, user_hnd=0x8, ion client=31\n\n\n"
    },
    {
      "time": 1690881439.051535,
      "raw": " [ 08-01 18:17:20.676  3511: 3702 I/[Gralloc] ]\nddebug, free share_fd=71, user_hnd=0x9, ion client=31\n\n\n"
    },
    {
      "time": 1690881439.054968,
      "raw": " [ 08-01 18:17:20.675  4531: 4531 D/ToastUtil ]\nTranslateAnimator End\n\n"
    },
    {
      "time": 1690881439.058146,
      "raw": " [ 08-01 18:17:20.678  3561: 3561 I/[Gralloc] ]\nddebug, free share_fd=90, user_hnd=0x9, ion client=26\n\n\n"
    },
    {
      "time": 1690881439.061896,
      "raw": " [ 08-01 18:17:20.682  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3564, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.068595,
      "raw": " [ 08-01 18:17:20.683  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3564, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.072053,
      "raw": " [ 08-01 18:17:20.686  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3564, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.077171,
      "raw": " [ 08-01 18:17:20.696  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3584, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.092453,
      "raw": " [ 08-01 18:17:20.698  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3584, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.095209,
      "raw": " [ 08-01 18:17:20.702  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3584, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.097721,
      "raw": " [ 08-01 18:17:20.720  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3587, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.113173,
      "raw": " [ 08-01 18:17:20.721  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3587, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.113223,
      "raw": " [ 08-01 18:17:20.725  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3587, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.113236,
      "raw": " [ 08-01 18:17:20.740  3564: 3564 D/DEVICE   ]\nBTF|DEVICE_SetLedState|111|OUT| \n\n\n"
    },
    {
      "time": 1690881439.117859,
      "raw": " [ 08-01 18:17:20.740  2790: 2790 W/btvSocHalService-JNI ]\nbtvSocHalService_SetLedState::994 : out, opStatus:0 \n\n"
    },
    {
      "time": 1690881439.128083,
      "raw": " [ 08-01 18:17:20.741  4646: 4763 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState after jni, index: 3, status: 2, result: true\n\n"
    },
    {
      "time": 1690881439.130146,
      "raw": " [ 08-01 18:17:20.741  4646: 4763 W/BtvService_6.3.08 BtvJni[6]22.06.08 ]\nfrontPanelSetLedState take before ===============================================\n\n"
    },
    {
      "time": 1690881439.131849,
      "raw": " [ 08-01 18:17:20.755  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3596, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.153943,
      "raw": " [ 08-01 18:17:20.757  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3596, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.156388,
      "raw": " [ 08-01 18:17:20.760  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3596, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.159347,
      "raw": " [ 08-01 18:17:20.782  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3598, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.168258,
      "raw": " [ 08-01 18:17:20.782  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3598, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.176932,
      "raw": " [ 08-01 18:17:20.785  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3598, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.180743,
      "raw": " [ 08-01 18:17:20.795  3564:13946 I/LivePlayer_0 ]\nSEAN onCheckVoiceAssistant(mString: nugu_playback=off)\n\n"
    },
    {
      "time": 1690881439.183403,
      "raw": " [ 08-01 18:17:20.805  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3599, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.192844,
      "raw": " [ 08-01 18:17:20.806  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3599, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.192884,
      "raw": " [ 08-01 18:17:20.809  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3599, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.195717,
      "raw": " [ 08-01 18:17:20.820  3499: 3745 W/ServiceManagement ]\ngetService: unable to call into hwbinder service for vendor.amlogic.hardware.remotecontrol@1.0::IRemoteControl/default.\n\n"
    },
    {
      "time": 1690881439.195747,
      "raw": " [ 08-01 18:17:20.817  3499: 3499 W/ATVRemoteAudioH ]\ntype=1400 audit(0.0:3675904): avc: denied { call } for scontext=u:r:hal_audio_amlogic:s0 tcontext=u:r:rc_server:s0 tclass=binder permissive=0\n\n"
    },
    {
      "time": 1690881439.198718,
      "raw": " [ 08-01 18:17:20.820  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3602, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.207015,
      "raw": " [ 08-01 18:17:20.822  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3602, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.210131,
      "raw": " [ 08-01 18:17:20.825  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3602, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.212839,
      "raw": " [ 08-01 18:17:20.835  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3603, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.224194,
      "raw": " [ 08-01 18:17:20.836  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3603, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.227151,
      "raw": " [ 08-01 18:17:20.838  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3603, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.230107,
      "raw": " [ 08-01 18:17:20.852  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3604, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.233611,
      "raw": " [ 08-01 18:17:20.853  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3604, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.236411,
      "raw": " [ 08-01 18:17:20.856  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3604, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.236433,
      "raw": " [ 08-01 18:17:20.861  3587:15603 I/adbd     ]\nhost-72: read thread spawning\n\n"
    },
    {
      "time": 1690881439.236446,
      "raw": " [ 08-01 18:17:20.861  3587:15603 I/adbd     ]\nhost-72: read failed: Success\n\n"
    },
    {
      "time": 1690881439.236458,
      "raw": " [ 08-01 18:17:20.861  3587:15603 I/adbd     ]\nhost-72: connection terminated: read failed\n\n"
    },
    {
      "time": 1690881439.23647,
      "raw": " [ 08-01 18:17:20.861  3587:15604 I/adbd     ]\nhost-72: write thread spawning\n\n"
    },
    {
      "time": 1690881439.236481,
      "raw": " [ 08-01 18:17:20.861  3587: 3587 I/adbd     ]\nhost-72: already offline\n\n"
    },
    {
      "time": 1690881439.236501,
      "raw": " [ 08-01 18:17:20.861  3587: 3587 I/adbd     ]\ndestroying transport host-72\n\n"
    },
    {
      "time": 1690881439.236512,
      "raw": " [ 08-01 18:17:20.861  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-72): stopping\n\n"
    },
    {
      "time": 1690881439.236524,
      "raw": " [ 08-01 18:17:20.862  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-72): stopped\n\n"
    },
    {
      "time": 1690881439.241125,
      "raw": " [ 08-01 18:17:20.862  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-72): destructing\n\n"
    },
    {
      "time": 1690881439.245924,
      "raw": " [ 08-01 18:17:20.862  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-72): already stopped\n\n"
    },
    {
      "time": 1690881439.245953,
      "raw": " [ 08-01 18:17:20.869  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3605, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.290536,
      "raw": " [ 08-01 18:17:20.870  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3605, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.293369,
      "raw": " [ 08-01 18:17:20.873  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3605, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.296153,
      "raw": " [ 08-01 18:17:20.918  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3606, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.318964,
      "raw": " [ 08-01 18:17:20.919  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3606, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.320468,
      "raw": " [ 08-01 18:17:20.921  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3606, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.32358,
      "raw": " [ 08-01 18:17:20.947  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3607, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.348296,
      "raw": " [ 08-01 18:17:20.948  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3607, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.380664,
      "raw": " [ 08-01 18:17:20.950  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3607, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.380711,
      "raw": " [ 08-01 18:17:20.976  3963: 4465 W/bt_btm_ble ]\nbtm_ble_process_adv_pkt_cont device no longer discoverable, discarding advertising packet\n\n"
    },
    {
      "time": 1690881439.385734,
      "raw": " [ 08-01 18:17:20.989  3963: 4465 W/bt_btm_ble ]\nbtm_ble_process_adv_pkt_cont device no longer discoverable, discarding advertising packet\n\n"
    },
    {
      "time": 1690881439.390813,
      "raw": " [ 08-01 18:17:21.004  2790:13944 D/BOXKEY-STDVB ]\n[DEVICE 0] ++ remain buffer size : 28952\n\n"
    },
    {
      "time": 1690881439.390848,
      "raw": " [ 08-01 18:17:21.013  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3608, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.390861,
      "raw": " [ 08-01 18:17:21.015  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3608, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.390874,
      "raw": " [ 08-01 18:17:21.015  5372: 5372 D/BtvBtPairingService ]\nBT onDeviceAdded deviceName = 7D:9D:26:73:86:1C, mIsAutoPairing = true, mControlState = 0\n\n"
    },
    {
      "time": 1690881439.390885,
      "raw": " [ 08-01 18:17:21.018  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3608, size_up_to:49152\n\n"
    },
    {
      "time": 1690881439.403376,
      "raw": " [ 08-01 18:17:21.019  5372: 5372 D/BtvBluetoothUtils ]\nisBTControl name = 7D:9D:26:73:86:1C\n\n"
    },
    {
      "time": 1690881439.406122,
      "raw": " [ 08-01 18:17:21.019  5372: 5372 D/BluetoothEventManager ]\nDeviceFoundHandler created new CachedBluetoothDevice: 7D:9D:26:73:86:1C\n\n"
    },
    {
      "time": 1690881439.406145,
      "raw": " [ 08-01 18:17:21.031  5372: 5372 D/BtvBtPairingService ]\nBT onDeviceAdded deviceName = 48:FD:C8:1B:63:36, mIsAutoPairing = true, mControlState = 0\n\n"
    },
    {
      "time": 1690881439.411814,
      "raw": " [ 08-01 18:17:21.033  5372: 5372 D/BtvBluetoothUtils ]\nisBTControl name = 48:FD:C8:1B:63:36\n\n"
    },
    {
      "time": 1690881439.414678,
      "raw": " [ 08-01 18:17:21.033  5372: 5372 D/BluetoothEventManager ]\nDeviceFoundHandler created new CachedBluetoothDevice: 48:FD:C8:1B:63:36\n\n"
    },
    {
      "time": 1690881439.419276,
      "raw": " [ 08-01 18:17:21.039  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3609, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.43263,
      "raw": " [ 08-01 18:17:21.041  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3609, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.434494,
      "raw": " [ 08-01 18:17:21.045  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3609, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.43765,
      "raw": " [ 08-01 18:17:21.061  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3610, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.447002,
      "raw": " [ 08-01 18:17:21.062  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3610, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.449533,
      "raw": " [ 08-01 18:17:21.064  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3610, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.451532,
      "raw": " [ 08-01 18:17:21.074  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3615, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.48798,
      "raw": " [ 08-01 18:17:21.075  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3615, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.491606,
      "raw": " [ 08-01 18:17:21.078  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3615, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.49164,
      "raw": " [ 08-01 18:17:21.115  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3616, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.532465,
      "raw": " [ 08-01 18:17:21.116  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3616, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.535086,
      "raw": " [ 08-01 18:17:21.118  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3616, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.537994,
      "raw": " [ 08-01 18:17:21.160  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3618, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.549413,
      "raw": " [ 08-01 18:17:21.161  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3618, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.552252,
      "raw": " [ 08-01 18:17:21.164  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3618, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.555015,
      "raw": " [ 08-01 18:17:21.177  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3619, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.56093,
      "raw": " [ 08-01 18:17:21.178  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3619, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.563659,
      "raw": " [ 08-01 18:17:21.182  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3619, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.566587,
      "raw": " [ 08-01 18:17:21.187  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3620, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.568367,
      "raw": " [ 08-01 18:17:21.189  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3620, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.570215,
      "raw": " [ 08-01 18:17:21.193  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3620, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.572111,
      "raw": " [ 08-01 18:17:21.197  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3632, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.579831,
      "raw": " [ 08-01 18:17:21.198  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3632, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.582649,
      "raw": " [ 08-01 18:17:21.200  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3632, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.585402,
      "raw": " [ 08-01 18:17:21.207  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3636, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.591189,
      "raw": " [ 08-01 18:17:21.208  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3636, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.596056,
      "raw": " [ 08-01 18:17:21.212  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3636, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.599784,
      "raw": " [ 08-01 18:17:21.219  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:3637, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.602524,
      "raw": " [ 08-01 18:17:21.220  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:3637, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.66426,
      "raw": " [ 08-01 18:17:21.225  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:3637, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.668914,
      "raw": " [ 08-01 18:17:21.227  3564:13953 I/MiniAmVideoDec_0 ]\nvbuf:1028303/2097152, rp:0x854924b, latency:1284.61ms\n\n"
    },
    {
      "time": 1690881439.682334,
      "raw": " [ 08-01 18:17:21.291  3564:13967 I/HalAudioOutput ]\noutputRate:47970(1.00)\n\n"
    },
    {
      "time": 1690881439.684883,
      "raw": " [ 08-01 18:17:21.296  3564:13946 I/LivePlayer_0 ]\nSEAN onCheckVoiceAssistant(mString: nugu_playback=off)\n\n"
    },
    {
      "time": 1690881439.687912,
      "raw": " [ 08-01 18:17:21.310  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:4059, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.696389,
      "raw": " [ 08-01 18:17:21.311  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:4059, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.699153,
      "raw": " [ 08-01 18:17:21.315  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:4059, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.702839,
      "raw": " [ 08-01 18:17:21.321  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:4390, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.723944,
      "raw": " [ 08-01 18:17:21.324  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:4390, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.73449,
      "raw": " [ 08-01 18:17:21.331  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:4390, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.739155,
      "raw": " [ 08-01 18:17:21.350  2790:13937 E/libc     ]\nAccess denied finding property \"skb.audio.output\"\n\n"
    },
    {
      "time": 1690881439.744063,
      "raw": " [ 08-01 18:17:21.360  3963: 4122 D/bt_btif_config ]\nbtif_get_device_type: Device [74:83:c2:d1:3e:2e] type 2\n\n"
    },
    {
      "time": 1690881439.748499,
      "raw": " [ 08-01 18:17:21.345  2790: 2790 W/btvservice@1.0- ]\ntype=1400 audit(0.0:3675905): avc: denied { read } for name=\"u:object_r:default_prop:s0\" dev=\"tmpfs\" ino=189 scontext=u:r:btvservice_hal:s0 tcontext=u:object_r:default_prop:s0 tclass=file permissive=0\n\n"
    },
    {
      "time": 1690881439.751546,
      "raw": " [ 08-01 18:17:21.370  5372: 5372 D/BtvBtPairingService ]\nBT onDeviceAdded deviceName = OWP_37a1, mIsAutoPairing = true, mControlState = 0\n\n"
    },
    {
      "time": 1690881439.75158,
      "raw": " [ 08-01 18:17:21.371  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:4397, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.751594,
      "raw": " [ 08-01 18:17:21.376  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:4397, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.756179,
      "raw": " [ 08-01 18:17:21.376  5372: 5372 D/BtvBluetoothUtils ]\nisBTControl name = OWP_37a1\n\n"
    },
    {
      "time": 1690881439.764002,
      "raw": " [ 08-01 18:17:21.376  5372: 5372 D/BluetoothEventManager ]\nDeviceFoundHandler created new CachedBluetoothDevice: 59:8E:07:83:1A:57\n\n"
    },
    {
      "time": 1690881439.772365,
      "raw": " [ 08-01 18:17:21.382  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:4397, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.775577,
      "raw": " [ 08-01 18:17:21.391  3963: 3976 W/droid.bluetoot ]\nReducing the number of considered missed Gc histogram windows from 142 to 100\n\n"
    },
    {
      "time": 1690881439.775623,
      "raw": " [ 08-01 18:17:21.398  5372: 5372 D/BtvBtPairingService ]\nBT onDeviceAdded deviceName = UCK, mIsAutoPairing = true, mControlState = 0\n\n"
    },
    {
      "time": 1690881439.796301,
      "raw": " [ 08-01 18:17:21.401  5372: 5372 D/BtvBluetoothUtils ]\nisBTControl name = UCK\n\n"
    },
    {
      "time": 1690881439.799794,
      "raw": " [ 08-01 18:17:21.401  5372: 5372 D/BluetoothEventManager ]\nDeviceFoundHandler created new CachedBluetoothDevice: 74:83:C2:D1:3E:2E\n\n"
    },
    {
      "time": 1690881439.802646,
      "raw": " [ 08-01 18:17:21.424  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:4405, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.809351,
      "raw": " [ 08-01 18:17:21.424  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:4405, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.811949,
      "raw": " [ 08-01 18:17:21.428  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:4405, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.814937,
      "raw": " [ 08-01 18:17:21.436  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:7154, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.820523,
      "raw": " [ 08-01 18:17:21.437  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:7154, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.822078,
      "raw": " [ 08-01 18:17:21.441  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:7154, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.825435,
      "raw": " [ 08-01 18:17:21.445 15605:15605 D/AndroidRuntime ]\n>>>>>> START com.android.internal.os.RuntimeInit uid 2000 <<<<<<\n\n\n"
    },
    {
      "time": 1690881439.825469,
      "raw": " [ 08-01 18:17:21.449  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:13163, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.829102,
      "raw": " [ 08-01 18:17:21.452  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:13163, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.829143,
      "raw": " [ 08-01 18:17:21.453 15605:15605 I/AndroidRuntime ]\nUsing default boot image\n\n"
    },
    {
      "time": 1690881439.832947,
      "raw": " [ 08-01 18:17:21.453 15605:15605 I/AndroidRuntime ]\nLeaving lock profiling enabled\n\n"
    },
    {
      "time": 1690881439.835538,
      "raw": " [ 08-01 18:17:21.454  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:13163, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.837621,
      "raw": " [ 08-01 18:17:21.461 15605:15605 I/app_process ]\nCore platform API reporting enabled, enforcing=false\n\n"
    },
    {
      "time": 1690881439.840109,
      "raw": " [ 08-01 18:17:21.464  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:14799, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.848114,
      "raw": " [ 08-01 18:17:21.465  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:14799, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.85189,
      "raw": " [ 08-01 18:17:21.468  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:14799, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.854586,
      "raw": " [ 08-01 18:17:21.474  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:15073, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.864285,
      "raw": " [ 08-01 18:17:21.476  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:15073, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.867224,
      "raw": " [ 08-01 18:17:21.482  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:15073, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.86968,
      "raw": " [ 08-01 18:17:21.492  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:15088, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.879452,
      "raw": " [ 08-01 18:17:21.494  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:15088, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.882279,
      "raw": " [ 08-01 18:17:21.496  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:15088, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.886078,
      "raw": " [ 08-01 18:17:21.506  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:15518, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.898692,
      "raw": " [ 08-01 18:17:21.507  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:15518, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.902161,
      "raw": " [ 08-01 18:17:21.513  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:15518, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.90404,
      "raw": " [ 08-01 18:17:21.526  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:22153, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.908752,
      "raw": " [ 08-01 18:17:21.527  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:22153, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.912886,
      "raw": " [ 08-01 18:17:21.531  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:22153, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.915369,
      "raw": " [ 08-01 18:17:21.536  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:30963, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.918136,
      "raw": " [ 08-01 18:17:21.537  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:30963, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.92004,
      "raw": " [ 08-01 18:17:21.540  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:30963, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.92358,
      "raw": " [ 08-01 18:17:21.545  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:30969, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.9279,
      "raw": " [ 08-01 18:17:21.547  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:30969, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.931682,
      "raw": " [ 08-01 18:17:21.550  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:30969, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.934607,
      "raw": " [ 08-01 18:17:21.554  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:31009, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.940226,
      "raw": " [ 08-01 18:17:21.556  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:31009, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.944239,
      "raw": " [ 08-01 18:17:21.561  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:31009, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.952852,
      "raw": " [ 08-01 18:17:21.567  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:31052, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.952891,
      "raw": " [ 08-01 18:17:21.569  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:31052, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.952904,
      "raw": " [ 08-01 18:17:21.571  3518: 3518 D/memtrack_aml ]\ntype:2 for pid:31052, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.95292,
      "raw": " [ 08-01 18:17:21.574  3587:15607 I/adbd     ]\nhost-66: read thread spawning\n\n"
    },
    {
      "time": 1690881439.952932,
      "raw": " [ 08-01 18:17:21.574  3587:15607 I/adbd     ]\nhost-66: read failed: Success\n\n"
    },
    {
      "time": 1690881439.952944,
      "raw": " [ 08-01 18:17:21.574  3587:15607 I/adbd     ]\nhost-66: connection terminated: read failed\n\n"
    },
    {
      "time": 1690881439.952955,
      "raw": " [ 08-01 18:17:21.575  3587: 3587 I/adbd     ]\nhost-66: already offline\n\n"
    },
    {
      "time": 1690881439.952967,
      "raw": " [ 08-01 18:17:21.575  3587: 3587 I/adbd     ]\ndestroying transport host-66\n\n"
    },
    {
      "time": 1690881439.952979,
      "raw": " [ 08-01 18:17:21.575  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-66): stopping\n\n"
    },
    {
      "time": 1690881439.956147,
      "raw": " [ 08-01 18:17:21.579  3587:15608 I/adbd     ]\nhost-66: write thread spawning\n\n"
    },
    {
      "time": 1690881439.956175,
      "raw": " [ 08-01 18:17:21.580  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-66): stopped\n\n"
    },
    {
      "time": 1690881439.956188,
      "raw": " [ 08-01 18:17:21.580  3518: 3518 D/memtrack_aml ]\ntype:0 for pid:31091, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.9562,
      "raw": " [ 08-01 18:17:21.580  3587: 3587 I/adbd     ]\nBlockingConnectionAdapter(host-66): destructing\n\n"
    },
    {
      "time": 1690881439.956212,
      "raw": " [ 08-01 18:17:21.580  3518: 3518 D/memtrack_aml ]\ntype:1 for pid:31091, size_up_to:0\n\n"
    },
    {
      "time": 1690881439.956212,
      "raw": " [ 08-03 20:08:12.927  3571:32726 I/LivePlayer_0 ]"
    }
  ]
pattern = r"\[\s(?P<timestamp>\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s*(?P<pid>\d+)\s*:\s*(?P<tid>\d+)\s*(?P<log_level>[\w])\/(?P<module>.*)\s*\](?:\n(?P<message>.*))?"
# pattern = r"\[\s(?P<timestamp>\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s*(?P<pid>\d+):\s?(?P<tid>\d+).*\n"

not_match_count = 0
for i, data in enumerate(datas):
    raw_data = data['raw']
    match = re.search(pattern, raw_data, re.DOTALL)
    if match:
        dic = match.groupdict()
        print(dic)
        print(type(dic))
    else:
        not_match_count += 1
        print(f'not match. {i}. {raw_data}')
print(f'datas: {len(datas)}, not match count: {not_match_count}')