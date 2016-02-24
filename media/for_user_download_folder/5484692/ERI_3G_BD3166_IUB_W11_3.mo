//================================================================//
// Project           : VNP-KienGiang                         //       
// Created By        : OMCKV2 VNP2                      //       
//Date/Time Created : Feb. 8, 2016, 9:39 p.m.   //
// Site              :ERI_3G_BD3166(3G_VHX-Tan-Dong-Hiep_BDG)            //
// RBS Id            :  3166                                // 
//================================================================//
// Running at Node       : RBS                                    //
//================================================================//
CREATE
(
    parent "ManagedElement=1,IpSystem=1"
    identity "1"
    moType IpAccessSctp
    exception none
    nrOfAttributes 2
        userLabel String "IpAccessSctp_1"
        ipAccessHostEtRef1 Ref "ManagedElement=1,IpSystem=1,IpAccessHostEt=1"
)
CREATE
(
    parent "ManagedElement=1,TransportNetwork=1"
    identity "1"
    moType Sctp
    exception none
    nrOfAttributes 13
        userLabel String "Sctp_1"
        numberOfAssociations Integer 2
        minimumRto Integer 10
        maximumRto Integer 40
        initialRto Integer 20
        associationMaxRtx Integer 12
        pathMaxRtx Integer 6
        maxUserDataSize Integer 556
        mBuffer Integer 16
        nThreshold Integer 12
        initialAdRecWin Integer 16384
        rpuId Ref "ManagedElement=1,SwManagement=1,ReliableProgramUniter=sctp_host"
        ipAccessSctpRef Ref "ManagedElement=1,IpSystem=1,IpAccessSctp=1"
)
CREATE
(
    parent "ManagedElement=1,NodeBFunction=1"
    identity "b3166"
    moType Iub
    exception none
    nrOfAttributes 4
        controlPlaneTransportOption Struct
        nrOfElements 2
            atm Boolean false
            ipV4 Boolean true
        userPlaneTransportOption Struct
        nrOfElements 2
            atm Boolean false
            ipV4 Boolean true
    rbsId Integer 3166
        userPlaneIpResourceRef Ref "ManagedElement=1,IpSystem=1,IpAccessHostEt=1"
)
///Set Duplex and Bitrate for RBS3000
///SET
///  (
///  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
///  exception none
///  operatingMode Struct
///     nrOfElements 2
///     autoNegotiation Boolean true
///     configuredSpeedDuplex Integer 4 
///  )
///
///SET
///  (
///  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=2,PlugInUnit=1,ExchangeTerminalIp=1,EthernetSwitch=1,EthernetSwitchPort=1"
///  exception none
///  ingressPeakBitrate Integer 1000
///  )
CREATE
(
    parent "ManagedElement=1,NodeBFunction=1,Iub=b3166"
    identity "1"
    moType NbapCommon
    exception none
    nrOfAttributes 4
        l2EstablishReqRetryT Integer 1
        auditRetransmissionT Integer 5
        l2EstablishSupervisionT Integer 30
        l3EstablishSupervisionT Integer 30
)
CREATE
(
    parent "ManagedElement=1,NodeBFunction=1,Iub=b3166"
    identity "1"
    moType NbapDedicated
    exception none
    nrOfAttributes 2
        l2EstablishReqRetryT Integer 1
        l2EstablishSupervisionT Integer 30
)
SET
(
   mo "ManagedElement=1,NodeBFunction=1"
   exception none
   nbapDscp Integer 40
)
///
SET
(
   mo "ManagedElement=1,IpOam=1,Ip=1"
   exception none
   dscp Integer 34
)
SET
(
  mo "ManagedElement=1,IpSystem=1,IpAccessHostEt=1"
  exception none
  ntpDscp Integer 40
)
ACTION
(
  actionName setDscpPbit
  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
  exception none
  nrOfParameters 2
    Integer 0
    Integer 0
  returnValue none
)
ACTION
(
   actionName setDscpPbit
   mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
   exception none
   nrOfParameters 2
      Integer 18
      Integer 2
   returnValue none
)
ACTION
(
  actionName setDscpPbit
  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
  exception none
  nrOfParameters 2
    Integer 34
    Integer 4
  returnValue none
)
ACTION
(
  actionName setDscpPbit
  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
  exception none
  nrOfParameters 2
     Integer 40
     Integer 5
  returnValue none
)
ACTION
(
actionName setDscpPbit
  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
  exception none
  nrOfParameters 2
     Integer 46
     Integer 5
  returnValue none
)
ACTION
(
  actionName setDscpPbit
  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
  exception none
  nrOfParameters 2
     Integer 20
     Integer 3
  returnValue none
)
ACTION
(
  actionName setDscpPbit
  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
  exception none
  nrOfParameters 2
     Integer 22
     Integer 3
  returnValue none
)
ACTION
(
  actionName setDscpPbit
  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
  exception none
  nrOfParameters 2
     Integer 26
     Integer 4
  returnValue none
)
ACTION
(
  actionName setDscpPbit
  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
  exception none
  nrOfParameters 2
     Integer 28
     Integer 4
  returnValue none
)
ACTION
(
  actionName setDscpPbit
  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
  exception none
  nrOfParameters 2
     Integer 30
     Integer 4
  returnValue none
)
ACTION
(
  actionName setDscpPbit
  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
  exception none
  nrOfParameters 2
    Integer 36
    Integer 5
  returnValue none
)
ACTION
(
  actionName setDscpPbit
  mo "ManagedElement=1,Equipment=1,Subrack=1,Slot=1,PlugInUnit=1,ExchangeTerminalIp=1,GigaBitEthernet=1"
  exception none
  nrOfParameters 2
    Integer 38
    Integer 5
  returnValue none
)
///Additional Configuration
ACTION                                                                  
(                                                                       
       actionName create                                                
       mo "ManagedElement=1,SwManagement=1,ConfigurationVersion=1"      
       exception none                                                   
       nrOfParameters 5                                                 
       String "CV_FINISH_IUB"                                
       String "1"                                          
       Integer 5                                           
       String "RBS_Engineer"                                    
       String "Loaded_Iub_script"                                 
       returnValue none                                                 
)                                                                                                                                              
ACTION                                                                  
(                                                                       
       actionName setStartable                                          
       mo "ManagedElement=1,SwManagement=1,ConfigurationVersion=1"      
       exception none                                                   
       nrOfParameters 1                                                 
       String "CV_FINISH_IUB"                                         
       returnValue none                                                 
)                                                                       
