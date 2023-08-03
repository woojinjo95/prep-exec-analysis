import re


datas = [
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
    }
  ]
pattern = r"\[\s(?P<timestamp>\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s*(?P<pid>\d+)\s*:\s*(?P<tid>\d+)\s*(?P<log_level>[\w])\/(?P<module>.*)\s*\]\n(?P<message>.*)\n"
# pattern = r"\[\s(?P<timestamp>\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\s*(?P<pid>\d+):\s?(?P<tid>\d+).*\n"

not_match_count = 0
for i, data in enumerate(datas):
    raw_data = data['raw']
    match = re.search(pattern, raw_data, re.DOTALL)
    if match:
        print(match.groupdict())
    else:
        not_match_count += 1
        print(f'not match. {i}. {raw_data}')
print(f'not match count: {not_match_count}')