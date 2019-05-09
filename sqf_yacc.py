import ply.yacc as pyacc
from sqf_lex import tokens
from var_handler import VarHandler
from classes.namespace import Namespace
import sys


var_handler = VarHandler()
terminators = {
    ';': 0,
    ',': 0,
}
is_interpreting = True  # This indicates whether the parser should pass the code as if it was being executed

literals = []

engine_functions = ('abs', 'acctime', 'acos', 'action', 'actionids', 'actionkeys', 'actionkeysimages', 'actionkeysnames', 'actionkeysnamesarray', 'actionname', 'actionparams', 'activateaddons', 'activatedaddons', 'activatekey', 'add3denconnection', 'add3deneventhandler', 'add3denlayer', 'addaction', 'addaction_tkoh', 'addbackpack', 'addbackpackcargo', 'addbackpackcargoglobal', 'addbackpackglobal', 'addcamshake', 'addcuratoraddons', 'addcuratorcameraarea', 'addcuratoreditableobjects', 'addcuratoreditingarea', 'addcuratorpoints', 'addeditorobject', 'addeventhandler', 'addforce', 'addgoggles', 'addgroupicon', 'addhandgunitem', 'addheadgear', 'additem', 'additemcargo', 'additemcargoglobal', 'additempool', 'additemtobackpack', 'additemtouniform', 'additemtovest', 'addlivestats', 'addmagazine', 'addmagazineammocargo', 'addmagazinecargo', 'addmagazinecargoglobal', 'addmagazineglobal', 'addmagazinepool', 'addmagazines', 'addmagazineturret', 'addmenu', 'addmenuitem', 'addmissioneventhandler', 'addmpeventhandler', 'addmusiceventhandler', 'addownedmine', 'addplayerscores', 'addprimaryweaponitem', 'addpublicvariableeventhandler', 'addrating', 'addresources', 'addscore', 'addscoreside', 'addsecondaryweaponitem', 'addswitchableunit', 'addteammember', 'addtoremainscollector', 'addtorque', 'adduniform', 'addvehicle', 'addvest', 'addwaypoint', 'addweapon', 'addweaponcargo', 'addweaponcargoglobal', 'addweaponglobal', 'addweaponitem', 'addweaponpool', 'addweaponturret', 'admin', 'agent', 'agents', 'agltoasl', 'aimedattarget', 'aimpos', 'airdensitycurvertd', 'airdensityrtd', 'airplanethrottle', 'airportside', 'aisfinishheal', 'alive', 'all3denentities', 'allairports', 'allcontrols', 'allcurators', 'allcutlayers', 'alldead', 'alldeadmen', 'alldisplays', 'allgroups', 'allmapmarkers', 'allmines', 'allmissionobjects', 'allow3dmode', 'allowcrewinimmobile', 'allowcuratorlogicignoreareas', 'allowdamage', 'isdamageallowed', 'allowdammage', 'allowfileoperations', 'allowfleeing', 'allowgetin', 'allowsprint', 'allplayers', 'allsimpleobjects', 'allsites', 'allturrets', 'allunits', 'allunitsuav', 'allvariables', 'ammo', 'ammoonpylon', 'and', 'animate', 'animatebay', 'animatedoor', 'animatepylon', 'animatesource', 'animationnames', 'animationphase', 'animationsourcephase', 'animationstate', 'append', 'apply', 'armorypoints', 'arrayintersect', 'asin', 'asltoagl', 'asltoatl', 'assert', 'assignascargo', 'assignascargoindex', 'assignascommander', 'assignasdriver', 'assignasgunner', 'assignasturret', 'assigncurator', 'assignedcargo', 'assignedcommander', 'assigneddriver', 'assignedgunner', 'assigneditems', 'assignedtarget', 'assignedteam', 'assignedvehicle', 'assignedvehiclerole', 'assignitem', 'assignteam', 'assigntoairport', 'atan', 'atan2', 'atg', 'atltoasl', 'attachedobject', 'attachedobjects', 'attachedto', 'attachobject', 'attachto', 'attackenabled', 'backpack', 'backpackcargo', 'backpackcontainer', 'backpackitems', 'backpackmagazines', 'backpackspacefor', 'batterychargertd', 'behaviour', 'benchmark', 'binocular', 'blufor', 'boundingbox', 'boundingboxreal', 'boundingcenter', 'breakout', 'breakto', 'briefingname', 'buildingexit', 'buildingpos', 'buldozer_loadnewroads', 'buldozer_reloadopermap', 'buttonaction', 'buttonsetaction', 'cadetmode', 'call', 'callextension', 'camcommand', 'camcommit', 'camcommitprepared', 'camcommitted', 'camconstuctionsetparams', 'camcreate', 'camdestroy', 'cameraeffect', 'cameraeffectenablehud', 'camerainterest', 'cameraon', 'cameraview', 'campaignconfigfile', 'campreload', 'campreloaded', 'campreparebank', 'campreparedir', 'campreparedive', 'campreparefocus', 'campreparefov', 'campreparefovrange', 'campreparepos', 'campreparerelpos', 'campreparetarget', 'camsetbank', 'camsetdir', 'camsetdive', 'camsetfocus', 'camsetfov', 'camsetfovrange', 'camsetpos', 'camsetrelpos', 'camsettarget', 'camtarget', 'camusenvg', 'canadd', 'canadditemtobackpack', 'canadditemtouniform', 'canadditemtovest', 'cancelsimpletaskdestination', 'canfire', 'canmove', 'canslingload', 'canstand', 'cansuspend', 'cantriggerdynamicsimulation', 'canunloadincombat', 'canvehiclecargo', 'captive', 'captivenum', 'case', 'catch', 'cbchecked', 'cbsetchecked', 'ceil', 'channelenabled', 'cheatsenabled', 'checkaifeature', 'checkvisibility', 'civilian', 'classname', 'clear3denattribute', 'clear3deninventory', 'clearallitemsfrombackpack', 'clearbackpackcargo', 'clearbackpackcargoglobal', 'cleargroupicons', 'clearitemcargo', 'clearitemcargoglobal', 'clearitempool', 'clearmagazinecargo', 'clearmagazinecargoglobal', 'clearmagazinepool', 'clearoverlay', 'clearradio', 'clearvehicleinit', 'clearweaponcargo', 'clearweaponcargoglobal', 'clearweaponpool', 'clientowner', 'closedialog', 'closedisplay', 'closeoverlay', 'collapseobjecttree', 'collect3denhistory', 'collectivertd', 'combatmode', 'commandartilleryfire', 'commandchat', 'commander', 'commandfire', 'commandfollow', 'commandfsm', 'commandgetout', 'commandingmenu', 'commandmove', 'commandradio', 'commandstop', 'commandsuppressivefire', 'commandtarget', 'commandwatch', 'comment', 'commitoverlay', 'compile', 'compilefinal', 'completedfsm', 'composetext', 'configclasses', 'configfile', 'confighierarchy', 'configname', 'confignull', 'configproperties', 'configsourceaddonlist', 'configsourcemod', 'configsourcemodlist', 'confirmsensortarget', 'connectterminaltouav', 'controlnull', 'controlsgroupctrl', 'copyfromclipboard', 'copytoclipboard', 'copywaypoints', 'cos', 'count', 'countenemy', 'countfriendly', 'countside', 'counttype', 'countunknown', 'create3dencomposition', 'create3denentity', 'createagent', 'createcenter', 'createdialog', 'creatediarylink', 'creatediaryrecord', 'creatediarysubject', 'createdisplay', 'creategeardialog', 'creategroup', 'createguardedpoint', 'createlocation', 'createmarker', 'createmarkerlocal', 'createmenu', 'createmine', 'createmissiondisplay', 'creatempcampaigndisplay', 'createsimpleobject', 'createsimpletask', 'createsite', 'createsoundsource', 'createtarget', 'createtask', 'createteam', 'createtrigger', 'createunit', 'createvehicle', 'createvehiclecrew', 'createvehiclelocal', 'crew', 'ctaddheader', 'ctaddrow', 'ctclear', 'ctcursel', 'ctdata', 'ctfindheaderrows', 'ctfindrowheader', 'ctheadercontrols', 'ctheadercount', 'ctremoveheaders', 'ctremoverows', 'ctrlactivate', 'ctrladdeventhandler', 'ctrlangle', 'ctrlanimatemodel', 'ctrlanimationphasemodel', 'ctrlautoscrolldelay', 'ctrlautoscrollrewind', 'ctrlautoscrollspeed', 'ctrlchecked', 'ctrlclassname', 'ctrlcommit', 'ctrlcommitted', 'ctrlcreate', 'ctrldelete', 'ctrlenable', 'ctrlenabled', 'ctrlfade', 'ctrlhtmlloaded', 'ctrlidc', 'ctrlidd', 'ctrlmapanimadd', 'ctrlmapanimclear', 'ctrlmapanimcommit', 'ctrlmapanimdone', 'ctrlmapcursor', 'ctrlmapmouseover', 'ctrlmapscale', 'ctrlmapscreentoworld', 'ctrlmapworldtoscreen', 'ctrlmodel', 'ctrlmodeldirandup', 'ctrlmodelscale', 'ctrlparent', 'ctrlparentcontrolsgroup', 'ctrlposition', 'ctrlremovealleventhandlers', 'ctrlremoveeventhandler', 'ctrlscale', 'ctrlsetactivecolor', 'ctrlsetangle', 'ctrlsetautoscrolldelay', 'ctrlsetautoscrollrewind', 'ctrlsetautoscrollspeed', 'ctrlsetbackgroundcolor', 'ctrlsetchecked', 'ctrlseteventhandler', 'ctrlsetfade', 'ctrlsetfocus', 'ctrlsetfont', 'ctrlsetfonth1', 'ctrlsetfonth1b', 'ctrlsetfonth2', 'ctrlsetfonth2b', 'ctrlsetfonth3', 'ctrlsetfonth3b', 'ctrlsetfonth4', 'ctrlsetfonth4b', 'ctrlsetfonth5', 'ctrlsetfonth5b', 'ctrlsetfonth6', 'ctrlsetfonth6b', 'ctrlsetfontheight', 'ctrlsetfontheighth1', 'ctrlsetfontheighth2', 'ctrlsetfontheighth3', 'ctrlsetfontheighth4', 'ctrlsetfontheighth5', 'ctrlsetfontheighth6', 'ctrlsetfontheightsecondary', 'ctrlsetfontp', 'ctrlsetfontpb', 'ctrlsetfontsecondary', 'ctrlsetforegroundcolor', 'ctrlsetmodel', 'ctrlsetmodeldirandup', 'ctrlsetmodelscale', 'ctrlsetpixelprecision', 'ctrlsetposition', 'ctrlsetscale', 'ctrlsetstructuredtext', 'ctrlsettext', 'ctrlsettextcolor', 'ctrlsettooltip', 'ctrlsettooltipcolorbox', 'ctrlsettooltipcolorshade', 'ctrlsettooltipcolortext', 'ctrlshow', 'ctrlshown', 'ctrltext', 'ctrltextheight', 'ctrltextwidth', 'ctrltype', 'ctrlvisible', 'ctrowcontrols', 'ctrowcount', 'ctsetcursel', 'ctsetdata', 'ctsetheadertemplate', 'ctsetrowtemplate', 'ctsetvalue', 'ctvalue', 'curatoraddons', 'curatorcamera', 'curatorcameraarea', 'curatorcameraareaceiling', 'curatorcoef', 'curatoreditableobjects', 'curatoreditingarea', 'curatoreditingareatype', 'curatormouseover', 'curatorpoints', 'curatorregisteredobjects', 'curatorselected', 'curatorwaypointcost', 'current3denoperation', 'currentchannel', 'currentcommand', 'currentmagazine', 'currentmagazinedetail', 'currentmagazinedetailturret', 'currentmagazineturret', 'currentmuzzle', 'currentnamespace', 'currenttask', 'currenttasks', 'currentthrowable', 'currentvisionmode', 'currentwaypoint', 'currentweapon', 'currentweaponmode', 'currentweaponturret', 'currentzeroing', 'cursorobject', 'cursortarget', 'customchat', 'customradio', 'cutfadeout', 'cutobj', 'cutrsc', 'cuttext', 'damage', 'date', 'datetonumber', 'daytime', 'deactivatekey', 'debriefingtext', 'debugfsm', 'debuglog', 'default', 'deg', 'delete3denentities', 'deleteat', 'deletecenter', 'deletecollection', 'deleteeditorobject', 'deletegroup', 'deletegroupwhenempty', 'deleteidentity', 'deletelocation', 'deletemarker', 'deletemarkerlocal', 'deleterange', 'deleteresources', 'deletesite', 'deletestatus', 'deletetarget', 'deleteteam', 'deletevehicle', 'deletevehiclecrew', 'deletewaypoint', 'detach', 'detectedmines', 'diag_activemissionfsms', 'diag_activescripts', 'diag_activesqfscripts', 'diag_activesqsscripts', 'diag_captureframe', 'diag_captureframetofile', 'diag_captureslowframe', 'diag_codeperformance', 'diag_drawmode', 'diag_enable', 'diag_enabled', 'diag_fps', 'diag_fpsmin', 'diag_frameno', 'diag_lightnewload', 'diag_list', 'diag_log', 'diag_logslowframe', 'diag_mergeconfigfile', 'diag_recordturretlimits', 'diag_resetshapes', 'diag_setlightnew', 'diag_ticktime', 'diag_toggle', 'dialog', 'diarysubjectexists', 'didjip', 'didjipowner', 'difficulty', 'difficultyenabled', 'difficultyenabledrtd', 'difficultyoption', 'direction', 'directsay', 'disableai', 'disablecollisionwith', 'disableconversation', 'disabledebriefingstats', 'disablemapindicators', 'disablenvgequipment', 'disableremotesensors', 'disableserialization', 'disabletiequipment', 'disableuavconnectability', 'disableuserinput', 'displayaddeventhandler', 'displayctrl', 'displaynull', 'displayparent', 'displayremovealleventhandlers', 'displayremoveeventhandler', 'displayseteventhandler', 'dissolveteam', 'distance', 'distance2d', 'distancesqr', 'distributionregion', 'do', 'do3denaction', 'doartilleryfire', 'for_do', 'dofire', 'dofollow', 'dofsm', 'dogetout', 'domove', 'doorphase', 'dostop', 'dosuppressivefire', 'dotarget', 'dowatch', 'drawarrow', 'drawellipse', 'drawicon', 'drawicon3d', 'drawline', 'drawline3d', 'drawlink', 'drawlocation', 'drawpolygon', 'drawrectangle', 'drawtriangle', 'driver', 'drop', 'dynamicsimulationdistance', 'dynamicsimulationdistancecoef', 'dynamicsimulationenabled', 'dynamicsimulationsystemenabled', 'east', 'echo', 'edit3denmissionattributes', 'editobject', 'editorseteventhandler', 'effectivecommander', 'else', 'emptypositions', 'enableai', 'enableaifeature', 'enableaimprecision', 'enableattack', 'enableaudiofeature', 'enableautostartuprtd', 'enableautotrimrtd', 'enablecamshake', 'enablecaustics', 'enablechannel', 'enablecollisionwith', 'enablecopilot', 'enablecopilot', 'enabledebriefingstats', 'enablediaglegend', 'enabledynamicsimulation', 'enabledynamicsimulationsystem', 'enableenddialog', 'enableengineartillery', 'enableenvironment', 'environmentenabled', 'enablefatigue', 'enablegunlights', 'enableinfopanelcomponent', 'enableirlasers', 'enablemimics', 'enablepersonturret', 'enableradio', 'enablereload', 'enableropeattach', 'enablesatnormalondetail', 'enablesaving', 'enablesentences', 'enablesimulation', 'enablesimulationglobal', 'enablestamina', 'enablestressdamage', 'enableteamswitch', 'enabletraffic', 'enableuavconnectability', 'enableuavwaypoints', 'enablevehiclecargo', 'enablevehiclesensor', 'enableweapondisassembly', 'endloadingscreen', 'endmission', 'enemy', 'engineon', 'enginesisonrtd', 'enginespowerrtd', 'enginesrpmrtd', 'enginestorquertd', 'entities', 'estimatedendservertime', 'estimatedtimeleft', 'evalobjectargument', 'everybackpack', 'everycontainer', 'exec', 'execeditorscript', 'execfsm', 'execvm', 'exit', 'exitwith', 'exp', 'expecteddestination', 'exportjipmessages', 'exportlandscapexyz', 'eyedirection', 'eyepos', 'face', 'faction', 'fademusic', 'faderadio', 'fadesound', 'fadespeech', 'failmission', 'false', 'fillweaponsfrompool', 'find', 'findif', 'findcover', 'finddisplay', 'findeditorobject', 'findemptyposition', 'findemptypositionready', 'findnearestenemy', 'setunloadincombat', 'finishmissioninit', 'finite', 'fire', 'fireattarget', 'firstbackpack', 'flag', 'flaganimationphase', 'flagowner', 'fleeing', 'floor', 'flyinheight', 'flyinheightasl', 'fog', 'fogforecast', 'fogparams', 'for', 'for_forspec', 'for_var', 'forceadduniform', 'forcedmap', 'forceend', 'forceflagtexture', 'forcefollowroad', 'forcemap', 'forcerespawn', 'forcespeed', 'forcewalk', 'forceweaponfire', 'forceweatherchange', 'foreach', 'foreachmember', 'foreachmemberagent', 'foreachmemberteam', 'forgettarget', 'format', 'formation', 'formationdirection', 'formationleader', 'formationmembers', 'formationposition', 'formationtask', 'formattext', 'formleader', 'freelook', 'friendly', 'from', 'fromeditor', 'fuel', 'fullcrew', 'gearidcammocount', 'gearslotammocount', 'gearslotdata', 'get3denactionstate', 'get3denattribute', 'get3dencamera', 'get3denconnections', 'get3denentity', 'get3denentityid', 'get3dengrid', 'get3deniconsvisible', 'get3denlayerentities', 'get3denlinesvisible', 'get3denmissionattribute', 'get3denmouseover', 'get3denselected', 'getaimingcoef', 'getallenvsoundcontrollers', 'getallhitpointsdamage', 'getallownedmines', 'getallsoundcontrollers', 'getammocargo', 'getanimaimprecision', 'getanimspeedcoef', 'getarray', 'getartilleryammo', 'getartillerycomputersettings', 'getartilleryeta', 'getassignedcuratorlogic', 'getassignedcuratorunit', 'getbackpackcargo', 'getbleedingremaining', 'getburningvalue', 'getcameraviewdirection', 'getcargoindex', 'getcenterofmass', 'getclientstate', 'getclientstatenumber', 'getcompatiblepylonmagazines', 'getconnecteduav', 'getcontainermaxload', 'getcursorobjectparams', 'getcustomaimcoef', 'getcustomsoundcontroller', 'getdammage', 'getdescription', 'getdir', 'getdirvisual', 'getdlcassetsusage', 'getdlcassetsusagebyname', 'getdlcs', 'geteditorcamera', 'geteditormode', 'geteditorobjectscope', 'getelevationoffset', 'getenvsoundcontroller', 'getfatigue', 'getforcedflagtexture', 'getfriend', 'getfsmvariable', 'getfuelcargo', 'getgroupicon', 'getgroupiconparams', 'getgroupicons', 'gethidefrom', 'gethit', 'gethitindex', 'gethitpointdamage', 'getitemcargo', 'getmagazinecargo', 'getmarkercolor', 'getmarkerpos', 'getmarkersize', 'getmarkertype', 'getmass', 'getmissionconfig', 'getmissionconfigvalue', 'getmissiondlcs', 'getmissionlayerentities', 'getmodelinfo', 'getmouseposition', 'getmusicplayedtime', 'getnumber', 'getobjectargument', 'getobjectchildren', 'getobjectdlc', 'getobjectmaterials', 'getobjectproxy', 'getobjecttextures', 'getobjecttype', 'getobjectviewdistance', 'getoxygenremaining', 'getpersonuseddlcs', 'getpilotcameradirection', 'getpilotcameraposition', 'getpilotcamerarotation', 'getpilotcameratarget', 'getplatenumber', 'getplayerchannel', 'getplayerscores', 'getplayeruid', 'getplayeruidold', 'getpos', 'getposasl', 'getposaslvisual', 'getposaslw', 'getposatl', 'getposatlvisual', 'getposvisual', 'getposworld', 'getpylonmagazines', 'getreldir', 'getrelpos', 'getremotesensorsdisabled', 'getrepaircargo', 'getresolution', 'getshadowdistance', 'getshotparents', 'getslingload', 'getsoundcontroller', 'getsoundcontrollerresult', 'getspeed', 'getstamina', 'getstatvalue', 'getsuppression', 'getterraingrid', 'getterrainheightasl', 'gettext', 'gettotaldlcusagetime', 'gettrimoffsetrtd', 'getunitloadout', 'getunittrait', 'getusermfdtext', 'getusermfdvalue', 'getvariable', 'getvehiclecargo', 'getweaponcargo', 'getweaponsway', 'getwingsorientationrtd', 'getwingspositionrtd', 'getworld', 'getwppos', 'glanceat', 'globalchat', 'globalradio', 'goggles', 'goto', 'group', 'groupchat', 'groupfromnetid', 'groupiconselectable', 'groupiconsvisible', 'groupid', 'groupowner', 'groupradio', 'groupselectedunits', 'groupselectunit', 'grpnull', 'gunner', 'gusts', 'halt', 'handgunitems', 'handgunmagazine', 'handgunweapon', 'handshit', 'hasinterface', 'haspilotcamera', 'hasweapon', 'hcallgroups', 'hcgroupparams', 'hcleader', 'hcremoveallgroups', 'hcremovegroup', 'hcselected', 'hcselectgroup', 'hcsetgroup', 'hcshowbar', 'hcshownbar', 'headgear', 'hidebehindscripted', 'hidebody', 'hideobject', 'hideobjectglobal', 'hideselection', 'hierarchyobjectscount', 'hint', 'hintc', 'hintcadet', 'hintsilent', 'hmd', 'hostmission', 'htmlload', 'hudmovementlevels', 'humidity', 'if', 'image', 'importallgroups', 'importance', 'in', 'inarea', 'inareaarray', 'incapacitatedstate', 'independent', 'inflame', 'inflamed', 'infopanel', 'infopanelcomponentenabled', 'infopanelcomponents', 'infopanels', 'ingameuiseteventhandler', 'inheritsfrom', 'initambientlife', 'inpolygon', 'inputaction', 'inrangeofartillery', 'inserteditorobject', 'intersect', 'is3den', 'is3denmultiplayer', 'isabletobreathe', 'isagent', 'isaimprecisionenabled', 'isarray', 'isautohoveron', 'isautonomous', 'isautotest', 'isbleeding', 'isburning', 'isclass', 'iscollisionlighton', 'iscopilotenabled', 'isdedicated', 'isdlcavailable', 'isengineon', 'isequalto', 'isequaltype', 'isequaltypeall', 'isequaltypeany', 'isequaltypearray', 'isequaltypeparams', 'isfilepatchingenabled', 'isflashlighton', 'isflatempty', 'isforcedwalk', 'isformationleader', 'isgroupdeletedwhenempty', 'ishidden', 'ishidebehindscripted', 'isinremainscollector', 'isinstructorfigureenabled', 'isirlaseron', 'iskeyactive', 'iskindof', 'islaseron', 'islighton', 'islocalized', 'ismanualfire', 'ismarkedforcollection', 'ismultiplayer', 'isnil', 'isnull', 'isnumber', 'isobjecthidden', 'isobjectrtd', 'isonroad', 'ispipenabled', 'ispipenabled', 'isplayer', 'isrealtime', 'isremoteexecuted', 'isremoteexecutedjip', 'isserver', 'isshowing3dicons', 'issimpleobject', 'issprintallowed', 'isstaminaenabled', 'issteammission', 'isstreamfriendlyuienabled', 'isstressdamageenabled', 'istext', 'istouchingground', 'isturnedout', 'istuthintsenabled', 'isuavconnectable', 'isuavconnected', 'isuicontext', 'isuniformallowed', 'isvehiclecargo', 'isvehicleradaron', 'isvehiclesensorenabled', 'iswalking', 'isweapondeployed', 'isweaponrested', 'itemcargo', 'items', 'itemswithmagazines', 'join', 'joinas', 'joinassilent', 'joinsilent', 'joinstring', 'kbadddatabase', 'kbadddatabasetargets', 'kbaddtopic', 'kbhastopic', 'kbreact', 'kbremovetopic', 'kbtell', 'kbwassaid', 'keyimage', 'keyname', 'knowsabout', 'targetknowledge', 'land', 'landat', 'landresult', 'language', 'lasertarget', 'lbadd', 'lbclear', 'lbcolor', 'lbcolorright', 'lbcursel', 'lbdata', 'lbdelete', 'lbisselected', 'lbpicture', 'lbpictureright', 'lbselection', 'lbsetcolor', 'lbsetcolorright', 'lbsetcursel', 'lbsetdata', 'lbsetpicture', 'lbsetpicturecolor', 'lbsetpicturecolordisabled', 'lbsetpicturecolorselected', 'lbsetpictureright', 'lbsetpicturerightcolor', 'lbsetpicturerightcolordisabled', 'lbsetpicturerightcolorselected', 'lbsettext', 'lbsettextright', 'lbsetselectcolor', 'lbsetselectcolorright', 'lbsetselected', 'lbsettooltip', 'lbsetvalue', 'lbsize', 'lbsort', 'lbsortbyvalue', 'lbtext', 'lbtextright', 'lbvalue', 'leader', 'leaderboarddeinit', 'leaderboardgetrows', 'leaderboardinit', 'leaderboardrequestrowsfriends', 'leaderboardsrequestuploadscore', 'leaderboardsrequestuploadscorekeepbest', 'leaderboardstate', 'leavevehicle', 'librarycredits', 'librarydisclaimers', 'lifestate', 'lightattachobject', 'lightdetachobject', 'lightison', 'lightnings', 'limitspeed', 'linearconversion', 'endl', 'linebreak', 'lineintersects', 'lineintersectsobjs', 'lineintersectssurfaces', 'lineintersectswith', 'linkitem', 'list', 'listobjects', 'listremotetargets', 'listvehiclesensors', 'ln', 'lnbaddarray', 'lnbaddcolumn', 'lnbaddrow', 'lnbclear', 'lnbcolor', 'lnbcurselrow', 'lnbdata', 'lnbdeletecolumn', 'lnbdeleterow', 'lnbgetcolumnsposition', 'lnbpicture', 'lnbsetcolor', 'lnbsetcolumnspos', 'lnbsetcurselrow', 'lnbsetdata', 'lnbsetpicture', 'lnbsettext', 'lnbsetvalue', 'lnbsize', 'lnbsort', 'lnbsortbyvalue', 'lnbtext', 'lnbvalue', 'load', 'loadabs', 'loadbackpack', 'loadfile', 'loadgame', 'loadidentity', 'loadmagazine', 'loadoverlay', 'loadstatus', 'loaduniform', 'loadvest', 'local', 'localize', 'locationnull', 'locationposition', 'lock', 'lockcamerato', 'lockcargo', 'lockdriver', 'locked', 'lockedcargo', 'lockeddriver', 'lockedturret', 'lockidentity', 'lockturret', 'lockwp', 'log', 'logentities', 'lognetwork', 'lognetworkterminate', 'lookat', 'lookatpos', 'magazinecargo', 'magazines', 'magazinesallturrets', 'magazinesammo', 'magazinesammocargo', 'magazinesammofull', 'magazinesdetail', 'magazinesdetailbackpack', 'magazinesdetailuniform', 'magazinesdetailvest', 'magazinesturret', 'magazineturretammo', 'mapanimadd', 'mapanimclear', 'mapanimcommit', 'mapanimdone', 'mapcenteroncamera', 'mapgridposition', 'markasfinishedonsteam', 'markeralpha', 'markerbrush', 'markercolor', 'markerdir', 'markerpos', 'markershape', 'markersize', 'markertext', 'markertype', 'max', 'members', 'menuaction', 'menuadd', 'menuchecked', 'menuclear', 'menucollapse', 'menudata', 'menudelete', 'menuenable', 'menuenabled', 'menuexpand', 'menuhover', 'menupicture', 'menusetaction', 'menusetcheck', 'menusetdata', 'menusetpicture', 'menusetvalue', 'menushortcut', 'menushortcuttext', 'menusize', 'menusort', 'menutext', 'menuurl', 'menuvalue', 'min', 'mineactive', 'minedetectedby', 'missionconfigfile', 'missiondifficulty', 'missionname', 'missionnamespace', 'missionstart', 'missionversion', 'mod', 'modeltoworld', 'modeltoworldvisual', 'modeltoworldvisualworld', 'modeltoworldworld', 'modparams', 'moonintensity', 'moonphase', 'morale', 'move', 'move3dencamera', 'moveinany', 'moveincargo', 'moveincommander', 'moveindriver', 'moveingunner', 'moveinturret', 'moveobjecttoend', 'moveout', 'movetarget', 'movetime', 'moveto', 'movetocompleted', 'movetofailed', 'musicvolume', 'name', 'namesound', 'nearentities', 'nearestbuilding', 'nearestlocation', 'nearestlocations', 'nearestlocationwithdubbing', 'nearestobject', 'nearestobjects', 'nearestterrainobjects', 'nearobjects', 'nearobjectsready', 'nearroads', 'nearsupplies', 'neartargets', 'needreload', 'netid', 'netobjnull', 'newoverlay', 'nextmenuitemindex', 'nextweatherchange', 'nil', 'nmenuitems', 'not', 'numberofenginesrtd', 'numbertodate', 'object', 'objectcurators', 'objectfromnetid', 'objectparent', 'objnull', 'objstatus', 'onbriefinggear', 'onbriefinggroup', 'onbriefingnotes', 'onbriefingplan', 'onbriefingteamswitch', 'oncommandmodechanged', 'ondoubleclick', 'oneachframe', 'ongroupiconclick', 'ongroupiconoverenter', 'ongroupiconoverleave', 'onhcgroupselectionchanged', 'onmapsingleclick', 'onplayerconnected', 'onplayerdisconnected', 'onpreloadfinished', 'onpreloadstarted', 'onshownewobject', 'onteamswitch', 'opencuratorinterface', 'opendlcpage', 'opendsinterface', 'openmap', 'opensteamapp', 'openyoutubevideo', 'opfor', 'or', 'ordergetin', 'overcast', 'overcastforecast', 'owner', 'param', 'params', 'parsenumber', 'parsesimplearray', 'parsetext', 'parsingnamespace', 'particlesquality', 'pi', 'pickweaponpool', 'pitch', 'pixelgrid', 'pixelgridbase', 'pixelgridnouiscale', 'pixelh', 'pixelw', 'playableslotsnumber', 'playableunits', 'playaction', 'playactionnow', 'player', 'playerrespawntime', 'playerside', 'playersnumber', 'playgesture', 'playmission', 'playmove', 'playmovenow', 'playmusic', 'playscriptedmission', 'playsound', 'playsound3d', 'position', 'position_location', 'posscreentoworld', 'positioncameratoworld', 'posworldtoscreen', 'ppeffectadjust', 'ppeffectcommit', 'ppeffectcommitted', 'ppeffectcreate', 'ppeffectdestroy', 'ppeffectenable', 'ppeffectenabled', 'ppeffectforceinnvg', 'precision', 'preloadcamera', 'preloadobject', 'preloadsound', 'preloadtitleobj', 'preloadtitlersc', 'preprocessfile', 'preprocessfilelinenumbers', 'primaryweapon', 'primaryweaponitems', 'primaryweaponmagazine', 'priority', 'private', 'processdiarylink', 'processinitcommands', 'productversion', 'profilename', 'profilenamespace', 'profilenamesteam', 'progressloadingscreen', 'progressposition', 'progresssetposition', 'publicvariable', 'publicvariableclient', 'publicvariableserver', 'pushback', 'pushbackunique', 'putweaponpool', 'queryitemspool', 'querymagazinepool', 'queryweaponpool', 'rad', 'radiochanneladd', 'radiochannelcreate', 'radiochannelremove', 'radiochannelsetcallsign', 'radiochannelsetlabel', 'radiovolume', 'rain', 'rainbow', 'random', 'rank', 'rankid', 'rating', 'rectangular', 'registeredtasks', 'registertask', 'reload', 'reloadenabled', 'remotecontrol', 'remoteexec', 'remoteexeccall', 'remoteexecutedowner', 'remove3denconnection', 'remove3deneventhandler', 'remove3denlayer', 'removeaction', 'removeall3deneventhandlers', 'removeallactions', 'removeallassigneditems', 'removeallcontainers', 'removeallcuratoraddons', 'removeallcuratorcameraareas', 'removeallcuratoreditingareas', 'removealleventhandlers', 'removeallhandgunitems', 'removeallitems', 'removeallitemswithmagazines', 'removeallmissioneventhandlers', 'removeallmpeventhandlers', 'removeallmusiceventhandlers', 'removeallownedmines', 'removeallprimaryweaponitems', 'removeallweapons', 'removebackpack', 'removebackpackglobal', 'removeclothing', 'removecuratoraddons', 'removecuratorcameraarea', 'removecuratoreditableobjects', 'removecuratoreditingarea', 'removedrawicon', 'removedrawlinks', 'removeeventhandler', 'removefromremainscollector', 'removegoggles', 'removegroupicon', 'removehandgunitem', 'removeheadgear', 'removeitem', 'removeitemfrombackpack', 'removeitemfromuniform', 'removeitemfromvest', 'removeitems', 'removemagazine', 'removemagazineglobal', 'removemagazines', 'removemagazinesturret', 'removemagazineturret', 'removemenuitem', 'removemissioneventhandler', 'removempeventhandler', 'removemusiceventhandler', 'removeownedmine', 'removeprimaryweaponitem', 'removesecondaryweaponitem', 'removesimpletask', 'removeswitchableunit', 'removeteammember', 'removeuniform', 'removevest', 'removeweapon', 'removeweaponattachmentcargo', 'removeweaponcargo', 'removeweaponglobal', 'removeweaponturret', 'reportremotetarget', 'requiredversion', 'resetcamshake', 'resetsubgroupdirection', 'resistance', 'resize', 'resources', 'respawnvehicle', 'restarteditorcamera', 'reveal', 'revealmine', 'reverse', 'reversedmousey', 'roadat', 'roadsconnectedto', 'roledescription', 'ropeattachedobjects', 'ropeattachedto', 'ropeattachenabled', 'ropeattachto', 'ropecreate', 'ropecut', 'ropedestroy', 'ropedetach', 'ropeendposition', 'ropelength', 'ropes', 'ropesetcargomass', 'ropeunwind', 'ropeunwound', 'rotorsforcesrtd', 'rotorsrpmrtd', 'round', 'runinitscript', 'safezoneh', 'safezonew', 'safezonewabs', 'safezonex', 'safezonexabs', 'safezoney', 'save3deninventory', 'savegame', 'saveidentity', 'savejoysticks', 'saveoverlay', 'saveprofilenamespace', 'savestatus', 'savevar', 'savingenabled', 'say', 'say2d', 'say3d', 'scopename', 'score', 'scoreside', 'screenshot', 'screentoworld', 'scriptdone', 'scriptname', 'scriptnull', 'scudstate', 'secondaryweapon', 'secondaryweaponitems', 'secondaryweaponmagazine', 'select', 'selectbestplaces', 'selectdiarysubject', 'selectededitorobjects', 'selecteditorobject', 'selectionnames', 'selectionposition', 'selectleader', 'selectmax', 'selectmin', 'selectnoplayer', 'selectplayer', 'selectrandom', 'selectrandomweighted', 'selectweapon', 'selectweaponturret', 'sendaumessage', 'sendsimplecommand', 'sendtask', 'sendtaskresult', 'sendudpmessage', 'servercommand', 'servercommandavailable', 'servercommandexecutable', 'servername', 'servertime', 'set', 'set3denattribute', 'set3denattributes', 'set3dengrid', 'set3deniconsvisible', 'set3denlayer', 'set3denlinesvisible', 'set3denlogictype', 'set3denmissionattribute', 'set3denmissionattributes', 'set3denmodelsvisible', 'set3denobjecttype', 'set3denselected', 'setacctime', 'setactualcollectivertd', 'setairplanethrottle', 'setairportside', 'setammo', 'setammocargo', 'setammoonpylon', 'setanimspeedcoef', 'setaperture', 'setaperturenew', 'setapurtd', 'setarmorypoints', 'setattributes', 'setautonomous', 'setbatterychargertd', 'setbatteryrtd', 'setbehaviour', 'setbleedingremaining', 'setbrakesrtd', 'setcameraeffect', 'setcamerainterest', 'setcamshakedefparams', 'setcamshakeparams', 'setcamuseti', 'setcaptive', 'setcenterofmass', 'setcollisionlight', 'setcombatmode', 'setcompassoscillation', 'setconvoyseparation', 'setcuratorcameraareaceiling', 'setcuratorcoef', 'setcuratoreditingareatype', 'setcuratorwaypointcost', 'setcurrentchannel', 'setcurrenttask', 'setcurrentwaypoint', 'setcustomaimcoef', 'setcustomsoundcontroller', 'setcustomweightrtd', 'setdamage', 'setdammage', 'setdate', 'setdebriefingtext', 'setdefaultcamera', 'setdestination', 'setdetailmapblendpars', 'setdir', 'setdirection', 'setdrawicon', 'setdriveonpath', 'setdropinterval', 'setdynamicsimulationdistance', 'setdynamicsimulationdistancecoef', 'seteditormode', 'seteditorobjectscope', 'seteffectcondition', 'setenginerpmrtd', 'setface', 'setfaceanimation', 'setfatigue', 'setfeaturetype', 'setflaganimationphase', 'setflagowner', 'flagside', 'flagtexture', 'setflagside', 'setflagtexture', 'setfog', 'setformation', 'setformationtask', 'setformdir', 'setfriend', 'setfromeditor', 'setfsmvariable', 'setfuel', 'setfuelcargo', 'setgroupicon', 'setgroupiconparams', 'setgroupiconsselectable', 'setgroupiconsvisible', 'setgroupid', 'setgroupidglobal', 'setgroupowner', 'setgusts', 'sethidebehind', 'sethit', 'sethitindex', 'sethitpointdamage', 'sethorizonparallaxcoef', 'sethudmovementlevels', 'setidentity', 'setimportance', 'setinfopanel', 'setleader', 'setlightambient', 'setlightattenuation', 'setlightbrightness', 'setlightcolor', 'setlightdaylight', 'setlightflaremaxdistance', 'setlightflaresize', 'setlightintensity', 'setlightnings', 'setlightuseflare', 'setlocalwindparams', 'setmagazineturretammo', 'setmarkeralpha', 'setmarkeralphalocal', 'setmarkerbrush', 'setmarkerbrushlocal', 'setmarkercolor', 'setmarkercolorlocal', 'setmarkerdir', 'setmarkerdirlocal', 'setmarkerpos', 'setmarkerposlocal', 'setmarkershape', 'setmarkershapelocal', 'setmarkersize', 'setmarkersizelocal', 'setmarkertext', 'setmarkertextlocal', 'setmarkertype', 'setmarkertypelocal', 'setmass', 'setmimic', 'setmouseposition', 'setmusiceffect', 'setmusiceventhandler', 'setname', 'setnamesound', 'setobjectarguments', 'setobjectmaterial', 'setobjectmaterialglobal', 'setobjectproxy', 'setobjecttexture', 'setobjecttextureglobal', 'setobjectviewdistance', 'setovercast', 'setowner', 'setoxygenremaining', 'setparticlecircle', 'setparticleclass', 'setparticlefire', 'setparticleparams', 'setparticlerandom', 'setpilotcameradirection', 'setpilotcamerarotation', 'setpilotcameratarget', 'setpilotlight', 'setpipeffect', 'setpitch', 'setplatenumber', 'setplayable', 'setplayerrespawntime', 'setpos', 'setposasl', 'setposasl2', 'setposaslw', 'setposatl', 'setposition', 'setposworld', 'setpylonloadout', 'setpylonspriority', 'setradiomsg', 'setrain', 'setrainbow', 'setrandomlip', 'setrank', 'setrectangular', 'setrepaircargo', 'setrotorbrakertd', 'setshadowdistance', 'setshotparents', 'setside', 'setsimpletaskalwaysvisible', 'setsimpletaskcustomdata', 'setsimpletaskdescription', 'setsimpletaskdestination', 'setsimpletasktarget', 'setsimpletasktype', 'setsimulweatherlayers', 'setsize', 'setskill', 'setslingload', 'setsoundeffect', 'setspeaker', 'setspeech', 'setspeedmode', 'setstamina', 'setstaminascheme', 'setstarterrtd', 'setstatvalue', 'setsuppression', 'setsystemofunits', 'settargetage', 'settaskmarkeroffset', 'settaskresult', 'settaskstate', 'setterraingrid', 'settext', 'setthrottlertd', 'settimemultiplier', 'settitleeffect', 'settonemapping', 'settonemappingparams', 'settrafficdensity', 'settrafficdistance', 'settrafficgap', 'settrafficspeed', 'settriggeractivation', 'settriggerarea', 'settriggerstatements', 'settriggertext', 'settriggertimeout', 'settriggertype', 'settype', 'setunconscious', 'ismultiplayersolo', 'setunitability', 'setunitloadout', 'setunitpos', 'setunitposweak', 'setunitrank', 'setunitrecoilcoefficient', 'setunittrait', 'setuseractiontext', 'setusermfdtext', 'setusermfdvalue', 'setvariable', 'setvectordir', 'setvectordirandup', 'setvectorup', 'setvehicleammo', 'setvehicleammodef', 'setvehiclearmor', 'setvehiclecargo', 'setvehicleid', 'setvehicleinit', 'setvehiclelock', 'setvehicleposition', 'setvehicleradar', 'setvehiclereceiveremotetargets', 'setvehiclereportownposition', 'setvehiclereportremotetargets', 'setvehicletipars', 'setvehiclevarname', 'setvelocity', 'setvelocitymodelspace', 'setvelocitytransformation', 'setviewdistance', 'setvisibleiftreecollapsed', 'setwantedrpmrtd', 'setwaves', 'setwaypointbehaviour', 'setwaypointcombatmode', 'setwaypointcompletionradius', 'setwaypointdescription', 'setwaypointforcebehaviour', 'setwaypointformation', 'setwaypointhouseposition', 'setwaypointloiterradius', 'setwaypointloitertype', 'setwaypointname', 'setwaypointposition', 'setwaypointscript', 'setwaypointspeed', 'setwaypointstatements', 'setwaypointtimeout', 'setwaypointtype', 'setwaypointvisible', 'setweaponreloadingtime', 'setwind', 'setwinddir', 'setwindforce', 'setwindstr', 'setwingforcescalertd', 'setwppos', 'show3dicons', 'showchat', 'showcinemaborder', 'showcommandingmenu', 'showcompass', 'showcuratorcompass', 'showgps', 'showhud', 'showlegend', 'showmap', 'shownartillerycomputer', 'shownchat', 'showncompass', 'showncuratorcompass', 'showneweditorobject', 'showngps', 'shownhud', 'shownmap', 'shownpad', 'shownradio', 'shownscoretable', 'shownuavfeed', 'shownwarrant', 'shownwatch', 'showpad', 'showradio', 'showscoretable', 'showsubtitles', 'showuavfeed', 'showwarrant', 'showwatch', 'showwaypoint', 'showwaypoints', 'side', 'sideambientlife', 'sidechat', 'sideempty', 'sideenemy', 'sidefriendly', 'sidelogic', 'sideradio', 'sideunknown', 'simpletasks', 'simulationenabled', 'simulclouddensity', 'simulcloudocclusion', 'simulinclouds', 'simulsethumidity', 'simulweathersync', 'sin', 'size', 'sizeof', 'skill', 'skillfinal', 'skiptime', 'sleep', 'sliderposition', 'sliderrange', 'slidersetposition', 'slidersetrange', 'slidersetspeed', 'sliderspeed', 'slingloadassistantshown', 'soldiermagazines', 'someammo', 'sort', 'soundvolume', 'spawn', 'speaker', 'speed', 'speedmode', 'splitstring', 'sqrt', 'squadparams', 'stance', 'startloadingscreen', 'step', 'stop', 'stopenginertd', 'stopped', 'str', 'sunormoon', 'supportinfo', 'suppressfor', 'surfaceiswater', 'surfacenormal', 'surfacetype', 'swimindepth', 'switch', 'switch_do', 'switchableunits', 'switchaction', 'switchcamera', 'switchgesture', 'switchlight', 'switchmove', 'synchronizedobjects', 'synchronizedtriggers', 'synchronizedwaypoints', 'synchronizeobjectsadd', 'synchronizeobjectsremove', 'synchronizetrigger', 'synchronizewaypoint', 'synchronizewaypoint_trigger', 'systemchat', 'systemofunits', 'tan', 'targets', 'targetsaggregate', 'targetsquery', 'taskalwaysvisible', 'taskchildren', 'taskcompleted', 'taskcustomdata', 'taskdescription', 'taskdestination', 'taskhint', 'taskmarkeroffset', 'tasknull', 'taskparent', 'taskresult', 'taskstate', 'tasktype', 'teammember', 'teammembernull', 'teamname', 'teams', 'teamswitch', 'teamswitchenabled', 'teamtype', 'terminate', 'terrainintersect', 'terrainintersectasl', 'terrainintersectatasl', 'text', 'textlog', 'textlogformat', 'tg', 'then', 'throttlertd', 'throw', 'time', 'timemultiplier', 'titlecut', 'titlefadeout', 'titleobj', 'titlersc', 'titletext', 'to', 'toarray', 'tofixed', 'tolower', 'tostring', 'toupper', 'triggeractivated', 'triggeractivation', 'triggerarea', 'triggerattachedvehicle', 'triggerattachobject', 'triggerattachvehicle', 'triggerdynamicsimulation', 'triggerstatements', 'triggertext', 'triggertimeout', 'triggertimeoutcurrent', 'triggertype', 'true', 'try', 'turretlocal', 'turretowner', 'turretunit', 'tvadd', 'tvclear', 'tvcollapse', 'tvcollapseall', 'tvcount', 'tvcursel', 'tvdata', 'tvdelete', 'tvexpand', 'tvexpandall', 'tvpicture', 'tvsetcolor', 'tvsetcursel', 'tvsetdata', 'tvsetpicture', 'tvsetpicturecolor', 'tvsetpicturecolordisabled', 'tvsetpicturecolorselected', 'tvsetpictureright', 'tvsetpicturerightcolor', 'tvsetpicturerightcolordisabled', 'tvsetpicturerightcolorselected', 'tvsettext', 'tvsettooltip', 'tvsetvalue', 'tvsort', 'tvsortbyvalue', 'tvtext', 'tvtooltip', 'tvvalue', 'type', 'typename', 'typeof', 'uavcontrol', 'uinamespace', 'uisleep', 'unassigncurator', 'unassignitem', 'unassignteam', 'unassignvehicle', 'underwater', 'uniform', 'uniformcontainer', 'uniformitems', 'uniformmagazines', 'unitaddons', 'unitaimposition', 'unitaimpositionvisual', 'unitbackpack', 'unitisuav', 'unitpos', 'unitready', 'unitrecoilcoefficient', 'units', 'unitsbelowheight', 'unlinkitem', 'unlockachievement', 'unregistertask', 'updatedrawicon', 'updatemenuitem', 'updateobjecttree', 'useaiopermapobstructiontest', 'useaisteeringcomponent', 'useaudiotimeformoves', 'userinputdisabled', 'vectoradd', 'vectorcos', 'vectorcrossproduct', 'vectordiff', 'vectordir', 'vectordirvisual', 'vectordistance', 'vectordistancesqr', 'vectordotproduct', 'vectorfromto', 'vectormagnitude', 'vectormagnitudesqr', 'vectormodeltoworld', 'vectormodeltoworldvisual', 'vectormultiply', 'vectornormalized', 'vectorup', 'vectorupvisual', 'vectorworldtomodel', 'vectorworldtomodelvisual', 'vehicle', 'vehiclecargoenabled', 'vehiclechat', 'vehicleradio', 'vehiclereceiveremotetargets', 'vehiclereportownposition', 'vehiclereportremotetargets', 'vehicles', 'vehiclevarname', 'velocity', 'velocitymodelspace', 'verifysignature', 'vest', 'vestcontainer', 'vestitems', 'vestmagazines', 'viewdistance', 'visiblecompass', 'visiblegps', 'visiblemap', 'visibleposition', 'visiblepositionasl', 'visiblescoretable', 'visiblewatch', 'waituntil', 'waves', 'waypointattachedobject', 'waypointattachedvehicle', 'waypointattachobject', 'waypointattachvehicle', 'waypointbehaviour', 'waypointcombatmode', 'waypointcompletionradius', 'waypointdescription', 'waypointforcebehaviour', 'waypointformation', 'waypointhouseposition', 'waypointloiterradius', 'waypointloitertype', 'waypointname', 'waypointposition', 'waypoints', 'waypointscript', 'waypointsenableduav', 'waypointshow', 'waypointspeed', 'waypointstatements', 'waypointtimeout', 'waypointtimeoutcurrent', 'waypointtype', 'waypointvisible', 'weaponaccessories', 'weaponaccessoriescargo', 'weaponcargo', 'weapondirection', 'weaponinertia', 'weaponlowered', 'weapons', 'weaponsitems', 'weaponsitemscargo', 'weaponstate', 'weaponsturret', 'weightrtd', 'west', 'wfsidetext', 'while', 'wind', 'winddir', 'windstr', 'wingsforcesrtd', 'with', 'worldname', 'worldsize', 'worldtomodel', 'worldtomodelvisual', 'worldtoscreen', 'bis_fnc_3dcredits', 'bis_fnc_3dencamera', 'bis_fnc_3dencontrolshint', 'bis_fnc_3dendiagcreatelist', 'bis_fnc_3dendiagfonts', 'bis_fnc_3dendiagmousecontrol', 'bis_fnc_3dendrawlocations', 'bis_fnc_3denentitymenu', 'bis_fnc_3denexportattributes', 'bis_fnc_3denexportoldsqm', 'bis_fnc_3denexportterrainbuilder', 'bis_fnc_3denflashlight', 'bis_fnc_3dengrid', 'bis_fnc_3denintel', 'bis_fnc_3deninterface', 'bis_fnc_3denlistlocations', 'bis_fnc_3denmissionpreview', 'bis_fnc_3denmoduledescription', 'bis_fnc_3denshowmessage', 'bis_fnc_3denstatusbar', 'bis_fnc_3dentoolbar', 'bis_fnc_3dentutorial', 'bis_fnc_3denvisionmode', 'bis_fnc_aan', 'bis_fnc_absspeed', 'bis_fnc_activateaddons', 'bis_fnc_addclassoo', 'bis_fnc_addcommmenuitem', 'bis_fnc_addcuratorareafromtrigger', 'bis_fnc_addcuratorchallenge', 'bis_fnc_addcuratoricon', 'bis_fnc_addevidence', 'bis_fnc_addrespawninventory', 'bis_fnc_showrespawnmenudisableitem', 'bis_fnc_addrespawnposition', 'bis_fnc_addscore', 'bis_fnc_addscriptedeventhandler', 'bis_fnc_addstackedeventhandler', 'bis_fnc_addsupportlink', 'bis_fnc_addtopairs', 'bis_fnc_addvirtualbackpackcargo', 'bis_fnc_addvirtualitemcargo', 'bis_fnc_garage', 'bis_fnc_addvirtualmagazinecargo', 'bis_fnc_addvirtualweaponcargo', 'bis_fnc_addweapon', 'bis_fnc_admin', 'bis_fnc_advhint', 'bis_fnc_advhintarg', 'bis_fnc_advhintcall', 'bis_fnc_advhintcredits', 'bis_fnc_advhintformat', 'bis_fnc_aircraftcatapultlaunch', 'bis_fnc_aircraftsystemsinit', 'bis_fnc_aircrafttailhook', 'bis_fnc_aircraftwingstatecheck', 'bis_fnc_aligntabs', 'bis_fnc_allsynchronizedobjects', 'bis_fnc_allturrets', 'bis_fnc_ambientanim', 'bis_fnc_ambientanimcombat', 'bis_fnc_exp_camp_playsubtitles', 'bis_fnc_initslidervalue', 'bis_fnc_showsubtitle', 'bis_fnc_weaponaddon', 'bis_fnc_ambientanimgetparams', 'bis_fnc_ambientblacklist', 'bis_fnc_ambientblacklistadd', 'bis_fnc_ambientboats', 'bis_fnc_ambientflyby', 'bis_fnc_ambienthelicopters', 'bis_fnc_ambientplanes', 'bis_fnc_ambientpostprocess', 'bis_fnc_animalbehaviour', 'bis_fnc_animalrandomization', 'bis_fnc_animalsitespawn', 'bis_fnc_animateflag', 'bis_fnc_animatetaskwaypoint', 'bis_fnc_animtype', 'bis_fnc_animviewer', 'bis_fnc_areequal', 'bis_fnc_areequalnotnil', 'bis_fnc_arefriendly', 'bis_fnc_arithmeticmean', 'arma_3_function_viewer', 'bis_fnc_arraycompare', 'bis_fnc_arrayfinddeep', 'bis_fnc_arrayinsert', 'bis_fnc_arraypop', 'bis_fnc_arraypush', 'bis_fnc_arraypushstack', 'bis_fnc_arrayshift', 'bis_fnc_arrayshuffle', 'bis_fnc_arrayunshift', 'bis_fnc_arsenal', 'bis_fnc_assignplayerrole', 'bis_fnc_basevehicle', 'bis_fnc_baseweapon', 'bis_fnc_basicbackpack', 'bis_fnc_basictask', 'bis_fnc_blackin', 'bis_fnc_blackout', 'bis_fnc_bleedtickets', 'bis_fnc_bloodeffect', 'bis_fnc_boundingboxcorner', 'bis_fnc_boundingboxdimensions', 'bis_fnc_boundingboxmarker', 'bis_fnc_boundingcircle', 'bis_fnc_briefinganimate', 'bis_fnc_briefinginit', 'bis_fnc_buildingpositions', 'bis_fnc_call', 'bis_fnc_callscriptedeventhandler', 'bis_fnc_camera', 'bis_fnc_cameraold', 'bis_fnc_camfollow', 'bis_fnc_caralarm', 'bis_fnc_cargoturretindex', 'bis_fnc_carrier01animatedeflectors', 'bis_fnc_carrier01catapultactionadd', 'bis_fnc_carrier01catapultactionremove', 'bis_fnc_carrier01catapultid', 'bis_fnc_carrier01catapultlockto', 'bis_fnc_carrier01crewinanim', 'bis_fnc_carrier01crewplayanim', 'bis_fnc_carrier01edendelete', 'bis_fnc_carrier01edeninit', 'bis_fnc_carrier01init', 'bis_fnc_carrier01posupdate', 'bis_fnc_changesupportradiochannel', 'bis_fnc_cinemaborder', 'bis_fnc_classmagazine', 'bis_fnc_classweapon', 'bis_fnc_codeperformance', 'bis_fnc_colorconfigtorgba', 'bis_fnc_colorrgbatohtml', 'bis_fnc_colorrgbatotexture', 'bis_fnc_colorrgbtohtml', 'bis_fnc_commsmenucreate', 'bis_fnc_commsmenutoggleavailability', 'bis_fnc_commsmenutogglevisibility', 'bis_fnc_compatibleitems', 'bis_fnc_completedcuratorchallengescount', 'bis_fnc_conditionalselect', 'bis_fnc_configextremes', 'bis_fnc_configpath', 'bis_fnc_configviewer', 'bis_fnc_consolidatearray', 'bis_fnc_controlconfigs', 'bis_fnc_convertunits', 'bis_fnc_countdown', 'bis_fnc_counter', 'bis_fnc_createlogrecord', 'bis_fnc_createmenu', 'bis_fnc_createobjectoo', 'bis_fnc_createruin', 'bis_fnc_credits', 'bis_fnc_credits_movie', 'bis_fnc_credits_movieconfig', 'bis_fnc_credits_moviesupport', 'bis_fnc_crewcount', 'bis_fnc_crossproduct', 'bis_fnc_crows', 'bis_fnc_ctrlfittotextheight', 'bis_fnc_ctrlsetscale', 'bis_fnc_ctrltextheight', 'bis_fnc_curatorattachobject', 'bis_fnc_curatorattributes', 'bis_fnc_curatorautomatic', 'bis_fnc_curatorautomaticpositions', 'bis_fnc_curatorchallengedestroyvehicle', 'bis_fnc_curatorchallengefindintel', 'bis_fnc_curatorchallengefireweapon', 'bis_fnc_curatorchallengegetinvehicle', 'bis_fnc_curatorchallengeilluminate', 'bis_fnc_curatorchallengespawnlightning', 'bis_fnc_curatorhint', 'bis_fnc_curatorobjectedited', 'bis_fnc_curatorobjectplaced', 'bis_fnc_curatorobjectregistered', 'bis_fnc_curatorobjectregisteredtable', 'bis_fnc_curatorpinged', 'bis_fnc_curatorrespawn', 'bis_fnc_curatorsaymessage', 'bis_fnc_curatorvisionmodes', 'bis_fnc_curatorwaypointplaced', 'bis_fnc_customgps', 'bis_fnc_customgpsvideo', 'bis_fnc_customgpsvideo', 'bis_fnc_cutdecimals', 'bis_fnc_damagechanged', 'bis_fnc_damagepulsing', 'bis_fnc_dataterminalanimate', 'bis_fnc_dataterminalcolor', 'bis_fnc_dbclasscheck', 'bis_fnc_dbclassid', 'bis_fnc_dbclassindex', 'bis_fnc_dbclasslist', 'bis_fnc_dbclassremove', 'bis_fnc_dbclassreturn', 'bis_fnc_dbclassset', 'bis_fnc_dbconfigpath', 'bis_fnc_dbimportconfig', 'bis_fnc_dbimportxml', 'bis_fnc_dbisclass', 'bis_fnc_dbisvalue', 'bis_fnc_dbprint', 'bis_fnc_dbsymbolclass', 'bis_fnc_dbsymbolvalue', 'bis_fnc_dbvaluecheck', 'bis_fnc_dbvalueid', 'bis_fnc_dbvalueindex', 'bis_fnc_dbvaluelist', 'bis_fnc_dbvalueremove', 'bis_fnc_dbvaluereturn', 'bis_fnc_dbvalueset', 'bis_fnc_decodeflags', 'bis_fnc_deletecounter', 'bis_fnc_deleteinventory', 'bis_fnc_deletetask', 'bis_fnc_deletevehiclecrew', 'bis_fnc_destroycity', 'bis_fnc_diagaar', 'bis_fnc_diagaarrecord', 'bis_fnc_diaganim', 'bis_fnc_diagbulletcam', 'bis_fnc_diagconfig', 'bis_fnc_diagfindmissingauthors', 'bis_fnc_diaghit', 'bis_fnc_diagkey', 'bis_fnc_diagkeylayout', 'bis_fnc_diagkeytest', 'bis_fnc_diagknownastarget', 'bis_fnc_diagknowntargets', 'bis_fnc_diagloop', 'bis_fnc_diagmacros', 'bis_fnc_diagmacrosauthor', 'bis_fnc_diagmacrosmapsize', 'bis_fnc_diagmacrosnamesound', 'bis_fnc_diagmacrosverify', 'bis_fnc_diagmissionpositions', 'bis_fnc_diagmissionweapons', 'bis_fnc_diagpreview', 'bis_fnc_diagpreviewcycle', 'bis_fnc_diagpreviewvehiclecrew', 'bis_fnc_diagradio', 'bis_fnc_diagvehicleicons', 'bis_fnc_diagwiki', 'bis_fnc_diaryhints', 'bis_fnc_diarymaps', 'bis_fnc_didjip', 'bis_fnc_dirindicator', 'bis_fnc_dirteffect', 'bis_fnc_dirto', 'bis_fnc_disableloading', 'bis_fnc_disablesaving', 'bis_fnc_displayclouds', 'bis_fnc_displaycolorget', 'bis_fnc_displaycolorset', 'bis_fnc_displaycontrols', 'bis_fnc_displayloading', 'bis_fnc_displaymission', 'bis_fnc_displayname', 'bis_fnc_displayresize', 'bis_fnc_distance2d', 'bis_fnc_distance2dsqr', 'bis_fnc_dotproduct', 'bis_fnc_drawao', 'bis_fnc_drawarrow', 'bis_fnc_drawcuratordeaths', 'bis_fnc_drawcuratorlocations', 'bis_fnc_drawcuratorrespawnmarkers', 'bis_fnc_drawminefields', 'bis_fnc_drawrespawnpositions', 'bis_fnc_dynamictext', 'bis_fnc_earthquake', 'bis_fnc_effectfired', 'bis_fnc_effectfiredartillery', 'bis_fnc_effectfiredflares', 'bis_fnc_effectfiredhelirocket', 'bis_fnc_effectfiredlongsmoke', 'bis_fnc_effectfiredrifle', 'bis_fnc_effectfiredrocket', 'bis_fnc_effectfiredsmokelauncher', 'bis_fnc_effectfiredsmokelauncher_boat', 'bis_fnc_effectkilled', 'bis_fnc_effectkilledairdestruction', 'bis_fnc_effectkilledairdestructionstage2', 'bis_fnc_effectkilledsecondaries', 'bis_fnc_effectplankton', 'bis_fnc_egobjectivevisualizer', 'bis_fnc_egobjectivevisualizerdraw', 'bis_fnc_egspectator', 'bis_fnc_egspectatorcamera', 'bis_fnc_egspectatorcamerapreparetarget', 'bis_fnc_egspectatorcameraresettarget', 'bis_fnc_egspectatorcamerasettarget', 'bis_fnc_egspectatorcameratick', 'bis_fnc_egspectatordraw2d', 'bis_fnc_egspectatordraw3d', 'bis_fnc_egspectatorgetunitstodraw', 'bis_fnc_ejectionseatrelease', 'bis_fnc_enablesaving', 'bis_fnc_encodeflags', 'bis_fnc_endloadingscreen', 'bis_fnc_endmission', 'bis_fnc_endmissionserver', 'bis_fnc_weaponcomponents', 'bis_fnc_enemydetected', 'bis_fnc_enemysides', 'bis_fnc_enemytargets', 'bis_fnc_error', 'bis_fnc_errormsg', 'bis_fnc_establishingshot', 'bis_fnc_estimatedtimeleft', 'bis_fnc_execfsm', 'bis_fnc_execremote', 'bis_fnc_executestackedeventhandler', 'bis_fnc_execvm', 'bis_fnc_exportcfggroups', 'bis_fnc_exportcfghints', 'bis_fnc_exportcfgmagazines', 'bis_fnc_exportcfgpatches', 'bis_fnc_exportcfgvehicles', 'bis_fnc_exportcfgvehiclesassetdb', 'bis_fnc_exportcfgweapons', 'bis_fnc_exportconfighierarchy', 'bis_fnc_exportcuratorcosttable', 'bis_fnc_exporteditorpreviews', 'bis_fnc_exportfunctionstowiki', 'bis_fnc_exportgroupformations', 'bis_fnc_exportguibaseclasses', 'bis_fnc_exportinventory', 'bis_fnc_exportmaptobitxt', 'bis_fnc_exportvehicle', 'bis_fnc_fadeeffect', 'bis_fnc_fatigueeffect', 'bis_fnc_feedbackinit', 'bis_fnc_feedbackmain', 'bis_fnc_ffvupdate', 'bis_fnc_filterstring', 'bis_fnc_findallnestedelements', 'bis_fnc_findextreme', 'bis_fnc_findinpairs', 'bis_fnc_findnestedelement', 'bis_fnc_findoverwatch', 'bis_fnc_findsafepos', 'bis_fnc_finishcuratorchallenge', 'bis_fnc_fire', 'bis_fnc_firedbombdemine', 'bis_fnc_firesupport', 'bis_fnc_firesupportcluster', 'bis_fnc_firesupportvirtual', 'bis_fnc_fixdate', 'bis_fnc_flameseffect', 'bis_fnc_flies', 'bis_fnc_forcecuratorinterface', 'bis_fnc_forceend', 'bis_fnc_formatcuratorchallengeobjects', 'bis_fnc_fps', 'bis_fnc_friendlysides', 'bis_fnc_ftlmanager', 'bis_fnc_functionmeta', 'bis_fnc_functionpath', 'bis_fnc_functionsdebug', 'bis_fnc_garage3den', 'bis_fnc_gc', 'bis_fnc_gcinit', 'bis_fnc_genericsentence', 'bis_fnc_genericsentenceinit', 'bis_fnc_geometricmean', 'bis_fnc_getangledelta', 'bis_fnc_getarea', 'bis_fnc_getcfg', 'bis_fnc_getcfgdata', 'bis_fnc_getcfgdataarray', 'bis_fnc_getcfgdatabool', 'bis_fnc_getcfgdataobject', 'bis_fnc_getcfgdatapool', 'bis_fnc_getcfgisclass', 'bis_fnc_getcfgsubclasses', 'bis_fnc_getcloudletparams', 'bis_fnc_getfactions', 'bis_fnc_getfrompairs', 'bis_fnc_getidc', 'bis_fnc_getidd', 'bis_fnc_getintersectionsundercursor', 'bis_fnc_getlinedist', 'bis_fnc_getname', 'bis_fnc_getnetmode', 'bis_fnc_getobjectbbd', 'bis_fnc_getparamvalue', 'bis_fnc_getpitchbank', 'bis_fnc_getrespawninventories', 'bis_fnc_getrespawnmarkers', 'bis_fnc_getrespawnpositions', 'bis_fnc_getservervariable', 'bis_fnc_getturrets', 'bis_fnc_getunitbyuid', 'bis_fnc_getunitinsignia', 'bis_fnc_getvehiclecustomization', 'bis_fnc_getvirtualbackpackcargo', 'bis_fnc_getvirtualitemcargo', 'bis_fnc_getvirtualmagazinecargo', 'bis_fnc_getvirtualweaponcargo', 'bis_fnc_greatestnum', 'bis_fnc_gridtopos', 'bis_fnc_groupfromnetid', 'bis_fnc_groupindicator', 'bis_fnc_groupvehicles', 'bis_fnc_guibackground', 'bis_fnc_guieditor', 'bis_fnc_guieffecttiles', 'bis_fnc_guigrid', 'bis_fnc_guigridtoprofile', 'bis_fnc_guihint', 'bis_fnc_guimessage', 'bis_fnc_guinewsfeed', 'bis_fnc_halo', 'bis_fnc_dynamicgroups', 'bis_fnc_halt', 'bis_fnc_healing', 'bis_fnc_healtheffects', 'bis_fnc_helicoptercanfly', 'bis_fnc_helicopterdamage', 'bis_fnc_helicoptergethitpoints', 'bis_fnc_helicopterseat', 'bis_fnc_helicopterseatmove', 'bis_fnc_helicoptertype', 'bis_fnc_help', 'bis_fnc_hextorgb', 'bis_fnc_highlightcontrol', 'bis_fnc_holdactionadd', 'bis_fnc_hudlimits', 'bis_fnc_importimagelinks', 'bis_fnc_incapacitatedeffect', 'bis_fnc_indicatebleeding', 'bis_fnc_infotext', 'bis_fnc_initammobox', 'bis_fnc_initcuratorattribute', 'bis_fnc_initdisplay', 'bis_fnc_initexpo', 'bis_fnc_initinspectable', 'bis_fnc_initintelobject', 'bis_fnc_initleaflet', 'bis_fnc_initlistnboxsorting', 'bis_fnc_initmodules', 'bis_fnc_initmultiplayer', 'bis_fnc_initparams', 'bis_fnc_initplayable', 'bis_fnc_initrespawn', 'bis_fnc_initrespawnbackpack', 'bis_fnc_initvehicle', 'bis_fnc_initvehiclecrew', 'bis_fnc_initvehiclekart', 'bis_fnc_initvirtualunit', 'bis_fnc_instring', 'bis_fnc_instructorfigure', 'bis_fnc_interpolateweather', 'bis_fnc_intrigger', 'bis_fnc_inv', 'bis_fnc_invadd', 'bis_fnc_invcodetoarray', 'bis_fnc_invremove', 'bis_fnc_invslots', 'bis_fnc_invslotsempty', 'bis_fnc_invslottype', 'bis_fnc_invstring', 'bis_fnc_isbuildingenterable', 'bis_fnc_iscampaign', 'bis_fnc_iscurator', 'bis_fnc_iscuratoreditable', 'bis_fnc_isdemo', 'bis_fnc_isforcedcuratorinterface', 'bis_fnc_isinfrontof', 'bis_fnc_isinsidearea', 'bis_fnc_isinzoom', 'bis_fnc_isleapyear', 'bis_fnc_isloading', 'bis_fnc_islocalized', 'bis_fnc_isposblacklisted', 'bis_fnc_isunitvirtual', 'bis_fnc_isthrowable', 'bis_fnc_itemtype', 'bis_fnc_jukebox', 'bis_fnc_kbcanspeak', 'bis_fnc_kbcreatedummy', 'bis_fnc_kbisspeaking', 'bis_fnc_kbmenu', 'bis_fnc_kbpriority', 'bis_fnc_kbsentence', 'bis_fnc_kbskip', 'bis_fnc_kbtell', 'bis_fnc_kbtelllocal', 'bis_fnc_kbtopicconfig', 'bis_fnc_keycode', 'bis_fnc_keypointsexport', 'bis_fnc_keypointsexportfromkml', 'bis_fnc_kmlimport', 'bis_fnc_lerp', 'bis_fnc_limitammunition', 'bis_fnc_limititems', 'bis_fnc_limitsupport', 'bis_fnc_limitweaponitems', 'bis_fnc_linearconversion', 'bis_fnc_listcuratorplayers', 'bis_fnc_listplayers', 'bis_fnc_livefeed', 'bis_fnc_livefeedeffects', 'bis_fnc_livefeedmoduleeffects', 'bis_fnc_livefeedmoduleinit', 'bis_fnc_livefeedmodulesetsource', 'bis_fnc_livefeedmodulesettarget', 'bis_fnc_livefeedsetsource', 'bis_fnc_livefeedsettarget', 'bis_fnc_livefeedterminate', 'bis_fnc_loadclass', 'bis_fnc_loadentry', 'bis_fnc_loadfunctions', 'bis_fnc_loadinventory', 'bis_fnc_loadvehicle', 'bis_fnc_localize', 'bis_fnc_locationdescription', 'bis_fnc_locations', 'bis_fnc_locweaponinfo', 'bis_fnc_log', 'bis_fnc_logformat', 'bis_fnc_loop', 'bis_fnc_lowestnum', 'bis_fnc_magazinesentitytype', 'bis_fnc_magnitude', 'bis_fnc_magnitudesqr', 'bis_fnc_managecuratoraddons', 'bis_fnc_managecuratorchallenges', 'bis_fnc_mapsize', 'bis_fnc_markercreate', 'bis_fnc_markerparams', 'bis_fnc_markerpath', 'bis_fnc_markertotrigger', 'bis_fnc_markwaypoints', 'bis_fnc_maxdiffarray', 'bis_fnc_mirrorcuratorsettings', 'bis_fnc_miscanim', 'bis_fnc_missilelaunchpositionfix', 'bis_fnc_missionconversations', 'bis_fnc_missionconversationslocal', 'bis_fnc_missionflow', 'bis_fnc_missionhandlers', 'bis_fnc_missionrespawntype', 'bis_fnc_missiontasks', 'bis_fnc_missiontaskslocal', 'bis_fnc_missiontimeleft', 'bis_fnc_moduleai', 'bis_fnc_moduleammo', 'bis_fnc_moduleanimals', 'bis_fnc_modulearsenal', 'bis_fnc_modulebleedtickets', 'bis_fnc_modulebootcampstage', 'bis_fnc_modulecas', 'bis_fnc_modulechat', 'bis_fnc_modulecombatgetin', 'bis_fnc_modulecountdown', 'bis_fnc_modulecovermap', 'bis_fnc_modulecreatediaryrecord', 'bis_fnc_modulecreateprojectile', 'bis_fnc_modulecurator', 'bis_fnc_modulecuratoraddaddons', 'bis_fnc_modulecuratoraddcameraarea', 'bis_fnc_modulecuratoraddeditableobjects', 'bis_fnc_modulecuratoraddeditingarea', 'bis_fnc_modulecuratoraddeditingareaplayers', 'bis_fnc_modulecuratoraddicon', 'bis_fnc_modulecuratoraddpoints', 'bis_fnc_modulecuratorsetattributes', 'bis_fnc_modulecuratorsetcamera', 'bis_fnc_modulecuratorsetcoefs', 'bis_fnc_modulecuratorsetcostsdefault', 'bis_fnc_modulecuratorsetcostsside', 'bis_fnc_modulecuratorsetcostsvehicleclass', 'bis_fnc_modulecuratorseteditingareatype', 'bis_fnc_modulecuratorsetobjectcost', 'bis_fnc_moduledamage', 'bis_fnc_moduledate', 'bis_fnc_modulediary', 'bis_fnc_moduledooropen', 'bis_fnc_moduleeffectsbubbles', 'bis_fnc_moduleeffectsemittercreator', 'bis_fnc_moduleeffectsfire', 'bis_fnc_moduleeffectsplankton', 'bis_fnc_moduleeffectsshells', 'bis_fnc_moduleeffectssmoke', 'bis_fnc_moduleendmission', 'bis_fnc_moduleexecute', 'bis_fnc_modulefdballoonairdestruction', 'bis_fnc_modulefdballoonwaterdestruction', 'bis_fnc_modulefdcpclear', 'bis_fnc_modulefdcpin', 'bis_fnc_modulefdcpout', 'bis_fnc_modulefdfademarker', 'bis_fnc_modulefdskeetdestruction', 'bis_fnc_modulefdstatsclear', 'bis_fnc_modulefiringdrill', 'bis_fnc_modulefriendlyfire', 'bis_fnc_modulefuel', 'bis_fnc_modulegenericradio', 'bis_fnc_modulegroupid', 'bis_fnc_modulehandle', 'bis_fnc_modulehealth', 'bis_fnc_modulehint', 'bis_fnc_modulehq', 'bis_fnc_moduleinit', 'bis_fnc_modulelightning', 'bis_fnc_modulemine', 'bis_fnc_modulemissionname', 'bis_fnc_modulemode', 'bis_fnc_modulemodules', 'bis_fnc_modulemptypedefense', 'bis_fnc_modulemptypegamemaster', 'bis_fnc_modulemptypegroundsupport', 'bis_fnc_modulemptypegroundsupportbase', 'bis_fnc_modulemptypesectorcontrol', 'bis_fnc_modulemptypeseize', 'bis_fnc_moduleobjective', 'bis_fnc_moduleobjectivefind', 'bis_fnc_moduleobjectivegetin', 'bis_fnc_moduleobjectivemove', 'bis_fnc_moduleobjectiveracecp', 'bis_fnc_moduleobjectiveracefinish', 'bis_fnc_moduleobjectiveracestart', 'bis_fnc_moduleobjectivesector', 'bis_fnc_moduleobjectivetarget', 'bis_fnc_modulepositioning', 'bis_fnc_moduleposter', 'bis_fnc_modulepostprocess', 'bis_fnc_moduleprojectile', 'bis_fnc_modulepunishment', 'bis_fnc_moduleradiochannelcreate', 'bis_fnc_modulerank', 'bis_fnc_modulerating', 'bis_fnc_moduleremotecontrol', 'bis_fnc_modulerespawninventory', 'bis_fnc_modulerespawnposition', 'bis_fnc_modulerespawntickets', 'bis_fnc_modulerespawnvehicle', 'bis_fnc_modulesavegame', 'bis_fnc_modulesector', 'bis_fnc_modulesfx', 'bis_fnc_moduleshowhide', 'bis_fnc_modulesimulationmanager', 'bis_fnc_moduleskill', 'bis_fnc_moduleskiptime', 'bis_fnc_modulesound', 'bis_fnc_modulestrategicmapimage', 'bis_fnc_modulestrategicmapinit', 'bis_fnc_modulestrategicmapmission', 'bis_fnc_modulestrategicmapopen', 'bis_fnc_modulestrategicmaporbat', 'bis_fnc_moduletaskcreate', 'bis_fnc_moduletasksetdescription', 'bis_fnc_moduletasksetdestination', 'bis_fnc_moduletasksetstate', 'bis_fnc_moduletimetrial', 'bis_fnc_moduletracers', 'bis_fnc_moduletrident', 'bis_fnc_moduletriggers', 'bis_fnc_modulettcpclear', 'bis_fnc_modulettcpin', 'bis_fnc_modulettcpout', 'bis_fnc_modulettcptrigger', 'bis_fnc_modulettcptriggerbehind', 'bis_fnc_modulettstatsclear', 'bis_fnc_moduleunits', 'bis_fnc_moduleunlockarea', 'bis_fnc_moduleunlockobject', 'bis_fnc_modulevolume', 'bis_fnc_moduleweather', 'bis_fnc_modulezoneprotection', 'bis_fnc_modulezonerestriction', 'bis_fnc_monthdays', 'bis_fnc_moveaction', 'bis_fnc_movein', 'bis_fnc_movetorespawnposition', 'bis_fnc_mp', 'bis_fnc_mpexec', 'bis_fnc_music', 'bis_fnc_nearesthelipad', 'bis_fnc_nearestnum', 'bis_fnc_nearestpoint', 'bis_fnc_nearestposition', 'bis_fnc_nearestroad', 'bis_fnc_netid', 'bis_fnc_neutralizeunit', 'bis_fnc_noflyzone', 'bis_fnc_noflyzonescreate', 'bis_fnc_noflyzonesexport', 'bis_fnc_numberdigits', 'bis_fnc_numbertext', 'bis_fnc_objectfromnetid', 'bis_fnc_objectheight', 'bis_fnc_objectsgrabber', 'bis_fnc_objectside', 'bis_fnc_objectsmapper', 'bis_fnc_objecttype', 'bis_fnc_objectvar', 'bis_fnc_ondiarychanged', 'bis_fnc_onend', 'bis_fnc_onload', 'bis_fnc_onplayerconnected', 'bis_fnc_openfieldmanual', 'bis_fnc_orbataddgroupoverlay', 'bis_fnc_orbatanimate', 'bis_fnc_orbatconfigpreview', 'bis_fnc_orbatgetgroupparams', 'bis_fnc_orbatopen', 'bis_fnc_orbatremovegroupoverlay', 'bis_fnc_orbatsetgroupfade', 'bis_fnc_orbatsetgroupparams', 'bis_fnc_orbattooltip', 'bis_fnc_ordinalnumber', 'bis_fnc_overviewauthor', 'bis_fnc_overviewdifficulty', 'bis_fnc_overviewmission', 'bis_fnc_overviewterrain', 'bis_fnc_overviewtimetrial', 'bis_fnc_packstaticweapon', 'bis_fnc_holdactionremove', 'bis_fnc_param', 'bis_fnc_paramcountdown', 'bis_fnc_paramdaytime', 'bis_fnc_paramguerfriendly', 'bis_fnc_paramin', 'bis_fnc_paramrespawntickets', 'bis_fnc_paramrevivebleedoutduration', 'bis_fnc_paramreviveduration', 'bis_fnc_paramreviveforcerespawnduration', 'bis_fnc_paramrevivemedicspeedmultiplier', 'bis_fnc_paramrevivemode', 'bis_fnc_paramreviverequireditems', 'bis_fnc_paramreviverequiredtrait', 'bis_fnc_paramreviveunconsciousstatemode', 'bis_fnc_paramviewdistance', 'bis_fnc_paramweather', 'bis_fnc_parsenumber', 'bis_fnc_phoneticalword', 'bis_fnc_pip', 'bis_fnc_planeaieject', 'bis_fnc_planeejection', 'bis_fnc_planeejectionfx', 'bis_fnc_playendmusic', 'bis_fnc_playername', 'bis_fnc_playersidefaction', 'bis_fnc_playmusic', 'bis_fnc_playsound', 'bis_fnc_playvideo', 'bis_fnc_posdegtoutm', 'bis_fnc_posdegtoworld', 'bis_fnc_position', 'bis_fnc_postogrid', 'bis_fnc_posutmtodeg', 'bis_fnc_preload', 'bis_fnc_prepareao', 'bis_fnc_progressloadingscreen', 'bis_fnc_quotations', 'bis_fnc_radialred', 'bis_fnc_radialredout', 'bis_fnc_radiosetchannel', 'bis_fnc_radiosetplaylist', 'bis_fnc_radiosettrack', 'bis_fnc_randomindex', 'bis_fnc_randomint', 'bis_fnc_randomnum', 'bis_fnc_randompos', 'bis_fnc_randompostrigger', 'bis_fnc_rankparams', 'bis_fnc_recompile', 'bis_fnc_refreshcommmenu', 'bis_fnc_registercuratorobject', 'bis_fnc_relativedirto', 'bis_fnc_relpos', 'bis_fnc_relposobject', 'bis_fnc_relscaleddist', 'bis_fnc_removeallscriptedeventhandlers', 'bis_fnc_removecommmenuitem', 'bis_fnc_removecuratoricon', 'bis_fnc_removedestroyedcuratoreditableobjects', 'bis_fnc_removefrompairs', 'bis_fnc_removeindex', 'bis_fnc_removenestedelement', 'bis_fnc_removerespawninventory', 'bis_fnc_removerespawnposition', 'bis_fnc_removescriptedeventhandler', 'bis_fnc_removestackedeventhandler', 'bis_fnc_removesupportlink', 'bis_fnc_removevirtualbackpackcargo', 'bis_fnc_removevirtualitemcargo', 'bis_fnc_removevirtualmagazinecargo', 'bis_fnc_removevirtualweaponcargo', 'bis_fnc_respawnbase', 'bis_fnc_respawnconfirm', 'bis_fnc_respawncounter', 'bis_fnc_respawnendmission', 'bis_fnc_respawngroup', 'bis_fnc_respawninstant', 'bis_fnc_respawnmanager', 'bis_fnc_respawnmenuinventory', 'bis_fnc_respawnmenuposition', 'bis_fnc_respawnmenuspectator', 'bis_fnc_respawnnone', 'bis_fnc_respawnrounds', 'bis_fnc_respawnseagull', 'bis_fnc_respawnside', 'bis_fnc_respawnspectator', 'bis_fnc_respawntickets', 'bis_fnc_respawntimepenalty', 'bis_fnc_respawnwave', 'bis_fnc_respect', 'bis_fnc_returnconfigentry', 'bis_fnc_returngroupcomposition', 'bis_fnc_returnnestedelement', 'bis_fnc_returnparents', 'bis_fnc_returnvehicleturrets', 'bis_fnc_romannumeral', 'bis_fnc_rotatevector2d', 'bis_fnc_rounddir', 'bis_fnc_roundnum', 'bis_fnc_rsclayer', 'bis_fnc_runlater', 'bis_fnc_sandstorm', 'bis_fnc_savegame', 'bis_fnc_saveinventory', 'bis_fnc_savevehicle', 'bis_fnc_saymessage', 'bis_fnc_sceneareaclearance', 'bis_fnc_scenecheckweapons', 'bis_fnc_scenecreatescenetrigger', 'bis_fnc_scenecreatesoundentities', 'bis_fnc_scenegetobjects', 'bis_fnc_scenegetparticipants', 'bis_fnc_scenegetpositionbyangle', 'bis_fnc_sceneintruderdetector', 'bis_fnc_scenemiscstuff', 'bis_fnc_scenerotate', 'bis_fnc_scenesetanimationsforgroup', 'bis_fnc_scenesetbehaviour', 'bis_fnc_scenesetobjects', 'bis_fnc_scenesetposformation', 'bis_fnc_scriptedmove', 'bis_fnc_scriptedwaypointtype', 'bis_fnc_secondstostring', 'bis_fnc_selectcrew', 'bis_fnc_selectdiarysubject', 'bis_fnc_selectrandom', 'bis_fnc_selectrandomweighted', 'bis_fnc_selectrespawntemplate', 'bis_fnc_setcuratorattributes', 'bis_fnc_setcuratorcamera', 'bis_fnc_setcuratorvisionmodes', 'bis_fnc_setdate', 'bis_fnc_setfog', 'bis_fnc_setheight', 'bis_fnc_sethitpointdamage', 'bis_fnc_setidcstreamfriendly', 'bis_fnc_setidentity', 'bis_fnc_setmissionstatusslot', 'bis_fnc_setnestedelement', 'bis_fnc_setobjectrotation', 'bis_fnc_setobjectshotparents', 'bis_fnc_setobjecttexture', 'bis_fnc_setovercast', 'bis_fnc_setpitchbank', 'bis_fnc_setppeffecttemplate', 'bis_fnc_setrank', 'bis_fnc_setrespawndelay', 'bis_fnc_setrespawninventory', 'bis_fnc_setservervariable', 'bis_fnc_settask', 'bis_fnc_settasklocal', 'bis_fnc_settopairs', 'bis_fnc_setunitinsignia', 'bis_fnc_setvehiclemass', 'bis_fnc_shakecuratorcamera', 'bis_fnc_shakegauges', 'bis_fnc_sharedobjectives', 'bis_fnc_showaanarticle', 'bis_fnc_showcuratorattributes', 'bis_fnc_showcuratorfeedbackmessage', 'bis_fnc_showmarkers', 'bis_fnc_showmissionstatus', 'bis_fnc_shownotification', 'bis_fnc_showrespawnmenu', 'bis_fnc_showrespawnmenudisableitemcheck', 'bis_fnc_showrespawnmenudisableitemdraw', 'bis_fnc_showrespawnmenuheader', 'bis_fnc_showrespawnmenuinventory', 'bis_fnc_showrespawnmenuinventorydetails', 'bis_fnc_showrespawnmenuinventoryitems', 'bis_fnc_showrespawnmenuinventorylimit', 'bis_fnc_showrespawnmenuinventorylimitrefresh', 'bis_fnc_showrespawnmenuinventorylimitrespawn', 'bis_fnc_showrespawnmenuinventorylist', 'bis_fnc_showrespawnmenuinventoryloadout', 'bis_fnc_showrespawnmenuinventorymetadata', 'bis_fnc_showrespawnmenuposition', 'bis_fnc_showrespawnmenupositionlist', 'bis_fnc_showrespawnmenupositionmap', 'bis_fnc_showrespawnmenupositionmapdraw', 'bis_fnc_showrespawnmenupositionmaphandle', 'bis_fnc_showrespawnmenupositionmetadata', 'bis_fnc_showrespawnmenupositionname', 'bis_fnc_showrespawnmenupositionrefresh', 'bis_fnc_showtime', 'bis_fnc_showunitinfo', 'bis_fnc_showwelcomescreen', 'bis_fnc_shutdown', 'bis_fnc_sideid', 'bis_fnc_sideisenemy', 'bis_fnc_sideisfriendly', 'bis_fnc_sidename', 'bis_fnc_sidenameunlocalized', 'bis_fnc_sidetype', 'bis_fnc_singlemissionconfig', 'bis_fnc_singlemissionkeys', 'bis_fnc_singlemissionname', 'bis_fnc_skirmishtrigger', 'bis_fnc_smoothstep', 'bis_fnc_sortalphabetically', 'bis_fnc_sortby', 'bis_fnc_sortnum', 'bis_fnc_spawn', 'bis_fnc_spawncrew', 'bis_fnc_spawnenemy', 'bis_fnc_spawngroup', 'bis_fnc_spawnobjects', 'bis_fnc_spawnvehicle', 'bis_fnc_splitstring', 'bis_fnc_spotter', 'bis_fnc_stalk', 'bis_fnc_startloadingscreen', 'bis_fnc_storeparamsvalues', 'bis_fnc_strategicmapanimate', 'bis_fnc_strategicmapmousebuttonclick', 'bis_fnc_strategicmapopen', 'bis_fnc_subclasses', 'bis_fnc_subselect', 'bis_fnc_sunrisesunsettime', 'bis_fnc_supplydrop', 'bis_fnc_supplydropservice', 'bis_fnc_swapvars', 'bis_fnc_synchronizedobjects', 'bis_fnc_target', 'bis_fnc_taskalwaysvisible', 'bis_fnc_taskattack', 'bis_fnc_taskchildren', 'bis_fnc_taskcompleted', 'bis_fnc_taskcreate', 'bis_fnc_taskcurrent', 'bis_fnc_taskdefend', 'bis_fnc_taskdescription', 'bis_fnc_taskdestination', 'bis_fnc_taskexists', 'bis_fnc_taskhandler', 'bis_fnc_taskhint', 'bis_fnc_taskparent', 'bis_fnc_taskpatrol', 'bis_fnc_taskreal', 'bis_fnc_tasksetalwaysvisible', 'bis_fnc_tasksetcurrent', 'bis_fnc_tasksetdescription', 'bis_fnc_tasksetdestination', 'bis_fnc_tasksetstate', 'bis_fnc_tasksettype', 'bis_fnc_taskstate', 'bis_fnc_tasksunit', 'bis_fnc_tasktype', 'bis_fnc_tasktypeicon', 'bis_fnc_taskvar', 'bis_fnc_teamcolor', 'bis_fnc_terraingradangle', 'bis_fnc_texttiles', 'bis_fnc_texturemarker', 'bis_fnc_texturevehicleicon', 'bis_fnc_threat', 'bis_fnc_titlecard', 'bis_fnc_titletext', 'bis_fnc_togglecuratorvisionmode', 'bis_fnc_toupperdisplaytexts', 'bis_fnc_tracebullets', 'bis_fnc_trackmissiontime', 'bis_fnc_transportservice', 'bis_fnc_tridentclient', 'bis_fnc_tridentexecute', 'bis_fnc_tridentgetrelationship', 'bis_fnc_tridenthandledamage', 'bis_fnc_tridentsetrelationship', 'bis_fnc_triggertomarker', 'bis_fnc_trimstring', 'bis_fnc_typetext', 'bis_fnc_typetext2', 'bis_fnc_uniqueclasses', 'bis_fnc_unitaddon', 'bis_fnc_unitcapture', 'bis_fnc_unitcapturefiring', 'bis_fnc_unitcapturesimple', 'bis_fnc_unitheadgear', 'bis_fnc_unitplay', 'bis_fnc_unitplayfiring', 'bis_fnc_unitplaysimple', 'bis_fnc_unitvector', 'bis_fnc_unpackstaticweapon', 'bis_fnc_updateplayerarray', 'bis_fnc_validateparametersoo', 'bis_fnc_variablespaceadd', 'bis_fnc_variablespaceremove', 'bis_fnc_vectoradd', 'bis_fnc_vectordiff', 'bis_fnc_vectorfromxtoy', 'bis_fnc_vectormultiply', 'bis_fnc_vehicleroles', 'bis_fnc_version', 'bis_fnc_versioninfo', 'bis_fnc_vrcourseballistics1', 'bis_fnc_vrcourseballistics2', 'bis_fnc_vrcourseballistics3', 'bis_fnc_vrcourseballistics4', 'bis_fnc_vrcoursecommandingactions1', 'bis_fnc_vrcoursecommandingactions2', 'bis_fnc_vrcoursecommandingactions3', 'bis_fnc_vrcoursecommandingbehaviour1', 'bis_fnc_vrcoursecommandingbehaviour2', 'bis_fnc_vrcoursecommandingbehaviour3', 'bis_fnc_vrcoursecommandingmovement1', 'bis_fnc_vrcoursecommandingmovement2', 'bis_fnc_vrcoursecommandingvehicles1', 'bis_fnc_vrcoursecommandingvehicles2', 'bis_fnc_vrcoursecommandingvehicles3', 'bis_fnc_vrcourseheliadvanced1', 'bis_fnc_vrcourseheliadvanced2', 'bis_fnc_vrcourseheliadvanced3', 'bis_fnc_vrcourseheliadvanced4', 'bis_fnc_vrcourseheliadvanced5', 'bis_fnc_vrcourseheliadvanced6', 'bis_fnc_vrcoursehelibasics1', 'bis_fnc_vrcoursehelibasics2', 'bis_fnc_vrcoursehelibasics3', 'bis_fnc_vrcoursehelislingload1', 'bis_fnc_vrcourseheliweapons1', 'bis_fnc_vrcourseheliweapons2', 'bis_fnc_vrcourseheliweapons3', 'bis_fnc_vrcourseheliweapons4', 'bis_fnc_vrcourselaunchers1', 'bis_fnc_vrcourselaunchers2', 'bis_fnc_vrcourselaunchers3', 'bis_fnc_vrcourseplaceables1', 'bis_fnc_vrcourseplaceables2', 'bis_fnc_vrcourseplaceables3', 'bis_fnc_vrcoursetargetdesignation1', 'bis_fnc_vrcoursetargetdesignation2', 'bis_fnc_vrcoursetargetdesignation3', 'bis_fnc_vrcourseweaponhandlinga1', 'bis_fnc_vrcourseweaponhandlinga2', 'bis_fnc_vrcourseweaponhandlinga3', 'bis_fnc_vrcourseweaponhandlingb1', 'bis_fnc_vrcourseweaponhandlingb2', 'bis_fnc_vrcourseweaponhandlingb3', 'bis_fnc_vrcourseweaponhandlingc1', 'bis_fnc_vrcourseweaponhandlingc2', 'bis_fnc_vrdrawborder', 'bis_fnc_vrdrawgrid', 'bis_fnc_vreffectkilled', 'bis_fnc_vrfadein', 'bis_fnc_vrfadeout', 'bis_fnc_vrhitpart', 'bis_fnc_vrspawneffect', 'bis_fnc_vrspawnselector', 'bis_fnc_vrtimer', 'bis_fnc_weaponsentitytype', 'bis_fnc_worldarea', 'bis_fnc_wpartillery', 'bis_fnc_wpdemine', 'bis_fnc_wpland_tkoh', 'bis_fnc_wppatrol', 'bis_fnc_wprelax', 'bis_fnc_wpsuppress', 'bis_fnc_zzrotate')

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'COMPARISON_OP', 'CONFIG_ACCESSOR_GTGT'),
    ('left', 'BINARY_OP', 'COLON'),
    ('left', 'ELSE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD', 'CONFIG_ACCESSOR_SLASH'),
    ('left', 'POW'),
    ('left', 'SELECT'),
    ('left', 'UNARY_OP'),
    ('left', 'NULAR_OP', 'VARIABLE', 'VALUE', 'BRACED_EXP'),
)


def p_code(p):
    """
    code    : empty
            | statement
            | statement terminator code
    """
    p[0] = p[len(p) - 1]


def p_statement(p):
    """
    statement   : controlstructure
                | assignment
                | binaryexp
                | nularexp
                | unaryexp
    """
    p[0] = p[1]


def p_terminator(p):
    """
    terminator  : SEMI_COLON
                | COMMA
    """
    terminators[p[1]] += 1
    if all(terminators.values()):
        semi_count = terminators.get(';')
        comma_count = terminators.get(',')
        if p[1] is not ';':
            print(f'WARNING: File contains mixed line terminators. "{p[1]}" seen on line: {p.lineno(1)}. '
                  f'Current count: (; {semi_count}), (, {comma_count}). '
                  f'Recommended to use ; as is standard.', file=sys.stderr)


def p_controlstructure(p):
    """
    controlstructure    : ifstatement
                        | whileloop
                        | forloop
                        | withstatement
    """
    p[0] = p[1]


def p_helpertype(p):
    """
    helpertype  : iftype
                | whiletype
                | fortype
                | withtype
    """
    p[0] = p[1]


def p_iftype(p):
    """
    iftype : IF LPAREN booleanexp RPAREN
    """
    p[0] = p[1]


def p_ifstatement(p):
    """
    ifstatement : iftype THEN bracedexp
                | iftype EXITWITH bracedexp
                | iftype THEN bracedexp ELSE bracedexp
    """
    p[0] = p[1]
    

def p_withtype(p):
    """
    withtype : WITH NAMESPACE
    """
    p[0] = Namespace(p[2])


def p_withstatementinit(p):
    """
    withstatementinit : withtype DO
    """
    if isinstance(p[1], Namespace):
        var_handler.change_namespace(p[1].value)
    else:
        print(f'WARNING: Possible error with WithType used on line: {p.lineno(1)}.')


def p_withstatement(p):
    """
    withstatement : withstatementinit bracedexp
    """
    p[0] = p[2]


def p_whiletype(p):
    """
    whiletype   : WHILE LBRACE booleanexp RBRACE
    """


def p_whileloop(p):
    """
    whileloop : whiletype DO bracedexp
    """
    p[0] = p[3]


def p_fortype(p):
    """
    fortype : FOR new_scope string FROM primaryexp TO primaryexp
            | FOR new_scope string FROM primaryexp TO primaryexp STEP primaryexp
            | FOR new_scope LSPAREN bracedexp_noscope COMMA forloop_condition COMMA bracedexp_noscope RSPAREN
    """
    if p[2] != '[':
        print(f'FORLOOP VAR: {p[2]}')


def p_forloop(p):
    """
    forloop : fortype DO bracedexp_noscope
    """
    var_handler.pop_local_stack()
    p[0] = p[3]
    

def p_bracedexp_condition(p):
    """
    forloop_condition   : LBRACE booleanexp RBRACE
                        | identifier
    """
    if len(p) is 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_bracedexp_noscope(p):
    """
     bracedexp_noscope : LBRACE code RBRACE
    """
    p[0] = p[2]


def p_assignment(p):
    """
    assignment  : assignment_code code RBRACE
                | definition EQUAL primaryexp
                | variable EQUAL primaryexp
    """
    if var_handler.has_local_var(p[1]):
        var_handler.add_local_var(p[1])
    elif p[1] in engine_functions:
        print(f'ERROR: Engine function assignment attempted on line: {p.lineno(1)}. '
              f'Engine functions cannot be assigned to.', file=sys.stderr)
    elif not p[1].startswith('_'):
        var_handler.add_global_var(p[1])
    if not get_interpretation_state():
        set_interpretation_state(True)


def p_assignment_code(p):
    """
    assignment_code : definition EQUAL LBRACE
                    | variable EQUAL LBRACE
    """
    #  Make parser read the braced code without "simulating" execution
    set_interpretation_state(False)
    p[0] = p[1]


def p_arraydefinition(p):
    """
    arraydefinition : PRIVATE stringarray
    """
    for index, element in enumerate(p[2]):
        element = element.replace('"', '')
        if var_handler.has_local_var(element):
            print(f'ERROR: Local variable {element} already defined. on line: {p.lineno(1)}.', file=sys.stderr)
        else:
            if element[0] is not '_':
                print(f'ERROR: Attempt to declare global variable {element} as private. on line: {p.lineno(1)}.', file=sys.stderr)
            if not element[1].islower():
                print(f'WARNING: Local variable {element} defined with unconventional casing. on line: {p.lineno(1)}. '
                      f'Use lower case for the first character of local variables.', file=sys.stderr)
            var_handler.add_local_var(element)


def p_definition(p):
    """
    definition : PRIVATE PRIVATE_ID
    """
    if var_handler.has_local_var(p[2]):
        global interpret
        if interpret:
            print(f'ERROR: Local variable {p[2]} already defined. on line: {p.lineno(2)}.', file=sys.stderr)
        p[0] = p[2]
    else:
        if not p[2][1].islower():
            print(f'WARNING: Local variable {p[2]} defined with unconventional casing. on line: {p.lineno(2)}. '
                  f'Use lower case for the first character of local variables.', file=sys.stderr)
        var_handler.add_local_var(p[2])
        p[0] = p[2]


def p_identifier(p):
    """
    identifier  : PRIVATE_ID %prec VARIABLE
                | GLOBAL_ID  %prec VARIABLE
    """
    if p[1].lower() in engine_functions:
        p[0] = p[1].lower()
    elif var_handler.has_local_var(p[1]):
        p[0] = var_handler.get_local_var(p[1])
    elif not p[1].startswith('_'):
        if var_handler.has_global_var(p[1]):
            p[0] = var_handler.get_global_var(p[1])
        else:
            var_handler.add_global_var(p[1])
            p[0] = p[1]
    else:
        if get_interpretation_state():
            print(f'ERROR: Undefined local variable ({p[1]}) used. on line {p.lineno(1)}.', file=sys.stderr)
        p[0] = p[1]


def p_variable(p):
    """
    variable    : PRIVATE_ID %prec VARIABLE
                | GLOBAL_ID %prec VARIABLE
    """
    p[0] = p[1]


def p_binaryexp(p):
    """
    binaryexp   : primaryexp BINARY_FNC primaryexp          %prec BINARY_OP
                | primaryexp comparisonoperator primaryexp  %prec BINARY_OP
                | primaryexp mathoperator primaryexp        %prec BINARY_OP
    """


def p_primaryexp(p):
    """
    primaryexp  : number                    %prec VALUE
                | identifier                %prec VALUE
                | helpertype                %prec VALUE
                | unaryexp                  %prec UNARY_OP
                | nularexp                  %prec NULAR_OP
                | string                    %prec VALUE
                | binaryexp                 %prec BINARY_OP
                | bracedexp                 %prec BRACED_EXP
                | LPAREN binaryexp RPAREN   %prec BRACED_EXP
                | array                     %prec VALUE
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_bracedexp(p):
    """
    bracedexp : LBRACE new_scope code RBRACE
    """
    p[0] = p[3]
    var_handler.pop_local_stack()


def p_new_scope(p):
    """new_scope :"""
    var_handler.new_local_scope()


def p_array(p):
    """
    array   : LSPAREN RSPAREN
            | LSPAREN arrayelement RSPAREN
    """
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]


def p_arrayelement(p):
    """
    arrayelement    : binaryexp
                    | binaryexp COMMA arrayelement
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[3]]


def p_stringarray(p):
    """
    stringarray : LSPAREN RSPAREN
                | LSPAREN stringarrayelement RSPAREN
    """
    if len(p) == 3:
        p[0] = []
    else:
        p[0] = p[2]


def p_stringarrayelement(p):
    """
    stringarrayelement  : string
                        | string COMMA stringarrayelement
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = [p[1], p[3]]


def p_nularexp(p):
    """
    nularexp    : NULAR_FNC     %prec NULAR_OP
                | identifier    %prec NULAR_OP
    """
    p[0] = p[1]
    

def p_unaryexp(p):
    """
    unaryexp    : UNARY_FNC primaryexp  %prec UNARY_OP
                | PLUS primaryexp       %prec UNARY_OP
                | MINUS primaryexp      %prec UNARY_OP
                | NOT primaryexp        %prec UNARY_OP
                | arraydefinition       %prec UNARY_OP
    """


def p_comparisonoperator(p):
    """
    comparisonoperator  : LT            %prec COMPARISON_OP
                        | GT            %prec COMPARISON_OP
                        | LTE           %prec COMPARISON_OP
                        | GTE           %prec COMPARISON_OP
                        | EQUALITY      %prec COMPARISON_OP
                        | INEQUALITY    %prec COMPARISON_OP
                        | AND           %prec COMPARISON_OP
                        | OR            %prec COMPARISON_OP
    """
    p[0] = p[1]


def p_mathoperator(p):
    """
    mathoperator : PLUS
                    | MINUS
                    | TIMES
                    | DIVIDE
                    | MOD
                    | POW
    """
    p[0] = p[1]


def p_booleanexp(p):
    """
    booleanexp  : primaryexp
                | primaryexp comparisonoperator booleanexp
                | primaryexp comparisonoperator LBRACE booleanexp RBRACE
    """


def p_configaccessor(p):
    """
    configaccessor  : GT GT     %prec CONFIG_ACCESSOR_GTGT
                    | DIVIDE    %prec CONFIG_ACCESSOR_SLASH
    """
    p[0] = ''.join(p[1:])


def p_number(p):
    """
    number  : NUMBER_REAL
            | NUMBER_EXP
            | NUMBER_HEX
    """
    p[0] = p[1]


def p_string(p):
    """
    string  : STRING_SINGLE
            | STRING_DOUBLE
    """
    p[0] = p[1]


def p_empty(p):
    """
    empty :
    """
    pass


def p_error(p):
    #
    if p:
        print('ERROR: Unexpected "{}" at line:{}, pos:{}\n'.format(p.value, p.lineno, p.lexpos), file=sys.stderr)
    else:
        print('ERROR: File possibly contains an incomplete statement.\n', file=sys.stderr)


def get_interpretation_state():
    global is_interpreting
    return is_interpreting


def set_interpretation_state(state):
    print(f'STATE::: setting state to: {state}')
    global is_interpreting
    is_interpreting = state


parser = pyacc.yacc()


def yacc():
    return parser
