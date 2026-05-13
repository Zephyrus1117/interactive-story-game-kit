#!/usr/bin/env python3
import json
from pathlib import Path


def seg(text, speaker=None, effect=None):
    item = {"text": text}
    if speaker:
        item["speaker"] = speaker
    if effect:
        item["effect"] = effect
    return item


def choice(text, next_id, val=0, flags=None, important=None, clues=None, items=None, rel=None, effect=None):
    changes = {}
    if val:
        changes["val"] = val
    if flags:
        changes["addFlags"] = flags
    if important:
        changes["importantFlag"] = {"flag": important[0], "label": important[1]}
    if clues:
        changes["addClue"] = clues[0] if len(clues) == 1 else clues[0]
        if len(clues) > 1:
            changes["addFlags"] = (changes.get("addFlags") or []) + clues[1:]
    if items:
        changes["addItem"] = items[0]
    if rel:
        changes["relationship"] = rel
    item = {"text": text, "next": next_id}
    if changes:
        item["changes"] = changes
    if effect:
        item["effect"] = effect
    return item


def node(title, scene, progress, segments, choices=None, routes=None, chapter=None, ambient="wind"):
    item = {
        "title": title,
        "scene": scene,
        "progress": progress,
        "ambient": ambient,
        "segments": segments,
    }
    if chapter:
        item["chapterTitle"] = chapter
    if choices:
        item["choices"] = choices
    if routes:
        item["routes"] = routes
    return item


def ending(title, etype, description, closing, achievement, ambient="wind"):
    return {
        "isEnding": True,
        "title": title,
        "type": etype,
        "progress": 100,
        "ambient": ambient,
        "achievement": achievement,
        "description": description,
        "closing": closing,
    }


scene_control = {
    "id": "control_room",
    "name": "十七号避难站控制室",
    "type": "major",
    "description": "三层防霜玻璃外是零下七十度的白夜，供暖核心的曲线在主屏上每分钟下降一点。",
    "arrival": "你把冻裂的手套放在台面上，听见远处有人在通风管里敲了三下。",
}

scene_hab = {
    "id": "hab_ring",
    "name": "居住环",
    "type": "major",
    "description": "隔热毯垂在走廊两侧，睡袋里传来压低的咳嗽声，墙上的霜像白色指纹。",
}

scene_green = {
    "id": "greenhouse",
    "name": "水培温室",
    "type": "major",
    "description": "冻裂的水槽里立着黑色菜根，玻璃穹顶被雪压得缓慢呻吟。",
}

scene_morgue = {
    "id": "morgue",
    "name": "临时停尸间",
    "type": "major",
    "description": "这里比走廊更冷。尸袋整齐地挂在滑轨上，每个标签都被霜盖住一半。",
}

scene_tunnel = {
    "id": "white_tunnel",
    "name": "白隧道",
    "type": "major",
    "description": "通往反应炉的地铁隧道已经停运，轨道之间堆着盐、破冰锤和没有归还的呼吸面罩。",
}

scene_lower = {
    "id": "lower_reactor",
    "name": "反应炉下层",
    "type": "major",
    "description": "热管像巨大的肋骨埋在墙里，红色应急灯把每个人的影子拉得很长。",
}

scene_nursery = {
    "id": "frost_nursery",
    "name": "霜巢育室",
    "type": "major",
    "description": "旧冷库被改成隔离区，玻璃后面漂着细小的白色孢丝，像一场不会落地的雪。",
}

scene_core = {
    "id": "core_chamber",
    "name": "供暖核心",
    "type": "major",
    "description": "反应炉心悬在黑井上方，最后的热光被霜雾啃成一圈暗红。",
}


nodes = {
    "start": node(
        "白昼不会升起",
        scene_control,
        3,
        [
            seg("极寒纪元第七年，太阳已经连续九天没有穿透风暴。你是十七号避难站的热工主管沈砚，今晚轮到你守供暖核心。", "系统", "cold"),
            seg("你的目标很清楚：找到失联的供暖核心巡检队，并决定是否重启地下反应炉。"),
            seg("如果反应炉在天亮前熄火，三千名避难者会在零下七十度的风暴里冻死。主屏上，核心温度正在跌破安全线。"),
        ],
        [
            choice("调出巡检队最后一次定位", "control_alarm", val=2, flags=["checked_locator"], clues=["last_locator"]),
            choice("先让警卫连岚封锁居住环", "speak_lian", val=-1, flags=["sealed_hab"], rel={"lian": 1}),
        ],
        chapter="第一章：白昼不会升起",
        ambient="wind",
    ),
    "control_alarm": node(
        "消失的四分钟",
        scene_control,
        6,
        [
            seg("定位记录显示，巡检队在 03:12 进入下层反应炉。03:16 后，四个人的生命体征同时变成一条白线。"),
            seg("系统没有报死亡。它给出的状态是：温度过低，身份待确认。"),
        ],
        [
            choice("复制定位记录到腕机", "check_log", val=3, flags=["copied_locator"], clues=["four_minute_gap"]),
            choice("把记录发给连岚，请她准备武装护送", "speak_lian", val=1, flags=["warned_lian"], rel={"lian": 1}),
        ],
        ambient="static",
    ),
    "speak_lian": node(
        "警卫的坏消息",
        scene_control,
        7,
        [
            seg("连岚推门进来，肩章上结着冰。她没有先问反应炉，只把一枚儿童手环放到你面前。"),
            seg("手环属于居住环的六岁女孩苏小禾。两小时前，她被登记为高烧；现在，她的体温记录是零下十二度。", "连岚"),
        ],
        [
            choice("要求连岚带你去医务室", "infirmary", val=1, flags=["saw_bracelet"], rel={"lian": 1}),
            choice("让连岚留守控制室，你独自查日志", "check_log", val=-2, flags=["left_lian_control"]),
        ],
    ),
    "check_log": node(
        "主控日志",
        scene_control,
        9,
        [
            seg("日志里有一条人工删除痕迹。删除者用的是你自己的权限，时间在你睡着后的 02:41。"),
            seg("被删内容只有一句：不要让他们把霜带进热里。"),
        ],
        [
            choice("承认权限异常，通知连岚", "speak_lian", val=2, flags=["admitted_breach"], rel={"lian": 1}),
            choice("暂时隐瞒权限异常，先去医务室看孩子", "infirmary", val=-4, flags=["hid_breach"], clues=["deleted_warning"]),
        ],
        ambient="static",
    ),
    "infirmary": node(
        "医务室里的冷汗",
        scene_hab,
        12,
        [
            seg("医务室挤满了人。加热灯全部打开，可墙角的水杯仍然结着冰。医生周泠把你拉到隔离帘后。"),
            seg("“不是冻伤。”周泠压低声音，“他们身体里有东西在主动降温，像在给自己造冬眠环境。”", "周泠"),
        ],
        [
            choice("检查苏小禾的病历", "patient_xiaohe", val=2, flags=["met_zhou"], clues=["cold_fever"]),
            choice("先去补给锁柜取热芯和破冰工具", "supply_lock", val=3, flags=["met_zhou"], items=["heat_cell"]),
        ],
    ),
    "patient_xiaohe": node(
        "孩子的纸条",
        scene_hab,
        14,
        [
            seg("苏小禾躺在保温袋里，睫毛上挂着霜。她没有睁眼，却把一张湿透的纸条攥得很紧。"),
            seg("纸条上写着：妈妈在炉子下面唱歌，她说那里很暖。"),
        ],
        [
            choice("把纸条收进证物袋", "supply_lock", val=2, flags=["took_child_note"], clues=["child_note"]),
            choice("把纸条交给周泠，请她安抚家属", "supply_lock", val=1, flags=["zhou_has_note"], rel={"zhou": 1}),
        ],
    ),
    "supply_lock": node(
        "补给锁柜",
        scene_hab,
        16,
        [
            seg("补给锁柜只剩两枚标准热芯、一把破冰锤和一支老式信号枪。管理系统要求你选择携带重量。"),
            seg("远处有人开始拍门，喊着医务室藏了感染者。避难站的恐慌比风暴更快。"),
        ],
        [
            choice("带上热芯和破冰锤", "choose_route", val=6, flags=["has_heat_cell", "has_ice_hammer"], items=["heat_cell"]),
            choice("带上信号枪和一枚热芯", "choose_route", val=3, flags=["has_flare", "has_heat_cell"], items=["flare_gun"]),
        ],
    ),
    "choose_route": node(
        "三条下行路",
        scene_hab,
        18,
        [
            seg("通往反应炉的主电梯已经停在负二层，不响应呼叫。你还可以穿过水培温室、临时停尸间，或从儿童区后面的维修楼梯下去。"),
            seg("连岚把步枪背带收紧：“选一条。再晚十分钟，居住环会开始抢热芯。”", "连岚"),
        ],
        [
            choice("穿过水培温室，寻找备用热管", "hydroponic_gate", val=2, flags=["route_greenhouse"]),
            choice("从停尸间旁边的检修门下去", "morgue_entry", val=-2, flags=["route_morgue"]),
            choice("走儿童区后面的维修楼梯", "nursery_hall", val=1, flags=["route_children"]),
        ],
    ),
    "hydroponic_gate": node(
        "冻裂的温室门",
        scene_green,
        21,
        [
            seg("温室门被冻在轨道里。门缝后面有水声，像有人在黑暗中轻轻洗手。"),
            seg("玻璃上从内侧写着两个字：别开。"),
        ],
        [
            choice("用破冰锤敲开门轨", "hydroponic_inside", val=-2, flags=["forced_greenhouse"], effect="shake"),
            choice("从维护管道绕进温室", "frozen_greenhouse", val=2, flags=["used_pipe"]),
        ],
        chapter="第二章：站内没有暖处",
    ),
    "hydroponic_inside": node(
        "水声",
        scene_green,
        23,
        [
            seg("你推门进去，水培槽里没有水，只有一层透明的霜。水声来自墙后的灌溉管，节奏像人类呼吸。"),
            seg("连岚举枪照向管道，里面有一截巡检队的袖标，被霜粘在阀门上。", "连岚"),
        ],
        [
            choice("剪下袖标作为证据", "seed_vault", val=1, flags=["took_sleeve"], clues=["team_sleeve"]),
            choice("沿着灌溉管追踪声音", "frozen_greenhouse", val=-3, flags=["followed_water_sound"]),
        ],
    ),
    "frozen_greenhouse": node(
        "白色根系",
        scene_green,
        25,
        [
            seg("你在菜根下发现白色丝状物。它们没有被冻死，反而绕着热管接口生长，像在寻找更暖的血管。"),
            seg("腕机提示：未知生物质。建议焚毁。"),
        ],
        [
            choice("用信号枪烧掉一片根系", "seed_vault", val=4, flags=["burned_roots"], clues=["white_roots"], effect="flash"),
            choice("取样保存，留给周泠分析", "seed_vault", val=-1, flags=["kept_sample"], clues=["white_roots"], items=["spore_sample"]),
        ],
    ),
    "seed_vault": node(
        "种子库",
        scene_green,
        27,
        [
            seg("种子库的冷柜全开着。冻雾中，一个巡检队员坐在地上，双手抱着胸牌。他的眼睛睁着，却没有瞳孔，只有一层白霜。"),
            seg("他的录音笔还在工作，重复播放同一句：不要重启，它们靠热醒来。"),
        ],
        [
            choice("取走录音笔", "maintenance_lift", val=2, flags=["has_recorder"], clues=["do_not_restart"]),
            choice("检查队员的胸牌和伤口", "dead_engineer", val=-2, flags=["checked_body"], clues=["frost_eyes"]),
        ],
    ),
    "morgue_entry": node(
        "停尸间门口",
        scene_morgue,
        21,
        [
            seg("停尸间外的温度计爆表，低温标尺已经到底。门后传来滑轨移动的声音，一格一格，像有人在挑选身体。"),
            seg("门禁记录显示，半小时前周泠来过这里。"),
        ],
        [
            choice("刷开停尸间门", "body_tags", val=-2, flags=["entered_morgue"]),
            choice("先追查周泠的门禁记录", "morgue_records", val=1, flags=["checked_zhou_access"], rel={"zhou": -1}),
        ],
    ),
    "morgue_records": node(
        "周泠的门禁",
        scene_morgue,
        23,
        [
            seg("记录显示，周泠带走了三具低温死亡者的肺部切片。备注栏写着：霜丝有记忆反应。"),
            seg("连岚看向你：“医生没有报告这个。你还信她吗？”", "连岚"),
        ],
        [
            choice("把记录发回控制室备份", "body_tags", val=2, flags=["backed_zhou_record"], clues=["zhou_samples"], rel={"lian": 1}),
            choice("删除周泠的违规记录，先保住医务室秩序", "body_tags", val=-4, flags=["protected_zhou"], rel={"zhou": 2}),
        ],
    ),
    "body_tags": node(
        "会变字的标签",
        scene_morgue,
        25,
        [
            seg("尸袋标签上的名字正在变化。你看见巡检队员的名字、苏小禾的名字，最后看见自己的名字。"),
            seg("冷柜深处，有人用指甲从内部刮门。"),
        ],
        [
            choice("打开刮响的冷柜", "dead_engineer", val=-4, flags=["opened_scratching_locker"], effect="shake"),
            choice("锁死冷柜，记录标签异常", "white_tunnel", val=2, flags=["locked_morgue"], clues=["shifting_tags"]),
        ],
    ),
    "dead_engineer": node(
        "还没死透的人",
        scene_morgue,
        28,
        [
            seg("冷柜里的巡检队员忽然吸气。他的胸腔发出冰面破裂的声音，嘴唇却只动出一个词：妈妈。"),
            seg("连岚后退半步。你看见他喉咙里有白色丝线，正在模仿声带。"),
        ],
        [
            choice("给他注射镇静剂，保留活体证据", "white_tunnel", val=-5, flags=["kept_host_alive"], clues=["speaking_frost"], rel={"zhou": 1}),
            choice("用热芯烧断霜丝，结束他的痛苦", "white_tunnel", val=5, flags=["burned_host"], clues=["speaking_frost"], effect="flash"),
        ],
    ),
    "nursery_hall": node(
        "儿童区后门",
        scene_hab,
        21,
        [
            seg("儿童区已经断电。墙上贴着孩子们画的太阳，每一张太阳都被人用白笔涂成了月亮。"),
            seg("你听见很多孩子在同一时间低声唱歌，歌词来自供暖核心的启动手册。"),
        ],
        [
            choice("进入宿舍确认孩子人数", "children_dorm", val=1, flags=["entered_children"]),
            choice("绕过宿舍，直奔护士站", "nurse_station", val=2, flags=["skipped_dorm"]),
        ],
    ),
    "children_dorm": node(
        "空床位",
        scene_hab,
        24,
        [
            seg("宿舍里只有空床。每个枕头中央都有一枚结霜的乳牙，按床号排成整齐的一列。"),
            seg("苏小禾的床下压着一个录音贴。"),
        ],
        [
            choice("播放录音贴", "dorm_recording", val=-1, flags=["played_child_recording"], clues=["child_song"]),
            choice("收起乳牙样本，继续下行", "nurse_station", val=1, flags=["took_teeth_sample"], clues=["frost_teeth"], items=["tooth_sample"]),
        ],
    ),
    "dorm_recording": node(
        "妈妈在炉下唱歌",
        scene_hab,
        26,
        [
            seg("录音里，苏小禾小声说：“妈妈说，冷不是死。冷是等春天。她让我把所有人带到炉子下面。”"),
            seg("录音结束后，走廊另一头响起孩子们的脚步声。人数不多，却像从每一面墙里走来。"),
        ],
        [
            choice("关掉录音，锁上儿童区门", "white_tunnel", val=2, flags=["sealed_children"], clues=["mother_under_core"]),
            choice("顺着脚步声追下维修楼梯", "nurse_station", val=-3, flags=["followed_children"], clues=["mother_under_core"]),
        ],
    ),
    "nurse_station": node(
        "护士站的热水",
        scene_hab,
        28,
        [
            seg("护士站的水壶还冒着热气。旁边的值班本记录着一个不可能的事实：失踪孩子每隔二十分钟回来喝一次水。"),
            seg("最后一行写着：他们说下层比这里暖。"),
        ],
        [
            choice("带走值班本", "white_tunnel", val=2, flags=["has_nurse_log"], clues=["children_return"]),
            choice("把热水分给走廊里的家属", "white_tunnel", val=-1, flags=["gave_hot_water"], rel={"station": 1}),
        ],
    ),
    "maintenance_lift": node(
        "卡住的货梯",
        scene_green,
        30,
        [
            seg("货梯卡在负一层，轿厢里挂着一件巡检队外套。外套内侧结着白霜，霜下写着一串数字：0316。"),
            seg("你记得那正是生命体征变白的时间。"),
        ],
        [
            choice("记录数字，改走白隧道", "white_tunnel", val=2, flags=["knows_0316"], clues=["0316"]),
            choice("强行启动货梯下降", "tunnel_pressure", val=-4, flags=["forced_lift"], effect="shake"),
        ],
    ),
    "white_tunnel": node(
        "白隧道入口",
        scene_tunnel,
        33,
        [
            seg("你们进入白隧道。风从反应炉方向吹来，却比身后的居住环更冷。轨道尽头亮着一点红光。"),
            seg("通讯里传来周泠的声音：“沈砚，如果你看见会说话的死人，不要回答它们的问题。”", "周泠"),
        ],
        [
            choice("询问周泠为什么知道死人会说话", "tunnel_pressure", val=2, flags=["questioned_zhou"], rel={"zhou": -1}),
            choice("关掉通讯，保持静默前进", "first_thing", val=1, flags=["radio_silent"]),
        ],
        chapter="第三章：白隧道",
    ),
    "tunnel_pressure": node(
        "压力门",
        scene_tunnel,
        36,
        [
            seg("压力门前堆着巡检队的工具箱。箱盖被人从内部顶开，里面装着四套整齐叠好的制服。"),
            seg("制服胸口的姓名牌被霜丝缝成一张脸。那张脸睁开眼，看向连岚。"),
        ],
        [
            choice("命令连岚后退，自己检查工具箱", "first_thing", val=2, flags=["protected_lian"], rel={"lian": 2}),
            choice("让连岚开枪打碎工具箱", "seal_door", val=-3, flags=["shot_toolbox"], rel={"lian": -1}, effect="flash"),
        ],
    ),
    "first_thing": node(
        "第一只白物",
        scene_tunnel,
        38,
        [
            seg("它从轨道下方爬出来，穿着巡检队的靴子，身体却像由冻雾和骨架临时拼成。"),
            seg("它没有攻击你，只用巡检队长的声音问：核心还热吗？"),
        ],
        [
            choice("回答它：核心还热，但正在降温", "seal_door", val=-2, flags=["answered_white"], clues=["white_asks_heat"]),
            choice("不开口，绕过它去开密封门", "seal_door", val=2, flags=["ignored_white"]),
            choice("用热芯逼退它", "reopen_or_bypass", val=4, flags=["repelled_white"], effect="flash"),
        ],
    ),
    "seal_door": node(
        "密封门",
        scene_tunnel,
        41,
        [
            seg("密封门的观察窗结着内霜。门后有人把手掌贴上来，五根手指都戴着巡检队的戒指。"),
            seg("门禁屏显示：下层仍有生命体征，数量十九。"),
        ],
        [
            choice("按规程开启密封门", "reactor_antechamber", val=-3, flags=["opened_seal"]),
            choice("先从旁通维修管道绕行", "reopen_or_bypass", val=2, flags=["used_bypass"]),
        ],
    ),
    "reopen_or_bypass": node(
        "旁通管道",
        scene_tunnel,
        43,
        [
            seg("旁通管道狭窄，隔热棉被撕开，里面塞满了孩子的画。每张画都画着同一个人：穿白衣的母亲，站在反应炉里。"),
            seg("你摸到一把冷库钥匙，钥匙柄上刻着周泠的编号。"),
        ],
        [
            choice("收起周泠的冷库钥匙", "reactor_antechamber", val=2, flags=["has_cold_key"], clues=["zhou_key"], items=["cold_storage_key"]),
            choice("把孩子的画拍照上传控制室", "reactor_antechamber", val=1, flags=["uploaded_drawings"], clues=["white_mother_drawings"]),
        ],
    ),
    "reactor_antechamber": node(
        "下层前室",
        scene_lower,
        46,
        [
            seg("前室的地面铺着一层薄薄的白霜。霜下封着许多手印，有成人，也有孩子。"),
            seg("墙上用巡检队的血写着：我们没有失踪，我们被留下看门。"),
        ],
        [
            choice("检查巡检队临时营地", "team_barracks", val=2, flags=["entered_lower"]),
            choice("直接去下层医务舱找幸存者", "medbay_lower", val=-1, flags=["rushed_medbay"]),
        ],
        chapter="第四章：反应炉下层",
        ambient="static",
    ),
    "team_barracks": node(
        "巡检队营地",
        scene_lower,
        48,
        [
            seg("睡袋被整齐割开，里面没有人，只有四堆还带着体温的霜。巡检队长卡普尔的平板压在工具箱下。"),
            seg("平板电量只够播放最后一段视频。"),
        ],
        [
            choice("播放卡普尔的视频", "kapoor_log", val=1, flags=["played_kapoor_log"], clues=["kapoor_video"]),
            choice("先搜工具箱找反应炉钥匙", "key_panel", val=3, flags=["searched_tools"]),
        ],
    ),
    "kapoor_log": node(
        "卡普尔的视频",
        scene_lower,
        50,
        [
            seg("视频里，卡普尔靠着反应炉井壁，脸上结霜。他说：“不是怪物闯进来，是我们把她挖出来了。”"),
            seg("“末世第一年，我们把第一批冻死者接进下层，用反应炉余热保存器官。白霜从那时开始学会了人的形状。”", "卡普尔"),
        ],
        [
            choice("把视频发给全站，公开真相", "lian_argument", val=4, flags=["broadcast_truth"], clues=["old_organ_storage"], rel={"station": -1}),
            choice("只发给连岚和周泠，避免恐慌", "lian_argument", val=1, flags=["shared_truth_small"], clues=["old_organ_storage"], rel={"lian": 1, "zhou": 1}),
        ],
    ),
    "lian_argument": node(
        "连岚的枪口",
        scene_lower,
        52,
        [
            seg("连岚听完视频，枪口垂下又抬起。“我妹妹就在第一批冻死者里。”她的声音很稳，“如果那些东西会学人，她可能也在下面。”", "连岚"),
            seg("你第一次意识到，重启反应炉不只是技术决定。热会救活三千人，也可能叫醒已经学会饥饿的死者。"),
        ],
        [
            choice("答应连岚，如果看见她妹妹就先确认身份", "medbay_lower", val=2, flags=["promised_lian"], rel={"lian": 2}),
            choice("坚持任务优先，任何白化体都不能放出", "medbay_lower", val=1, flags=["mission_first"], rel={"lian": -2}),
        ],
    ),
    "medbay_lower": node(
        "下层医务舱",
        scene_lower,
        53,
        [
            seg("下层医务舱的门半开，里面挂着十几袋冷凝血浆。周泠的肺部切片在显微镜下自己移动。"),
            seg("一个巡检队员被绑在病床上，胸口以下已经长成透明冰晶。"),
        ],
        [
            choice("询问被绑住的巡检队员", "frostbite_patient", val=-2, flags=["questioned_patient"]),
            choice("检查隔离窗后的样本", "containment_window", val=2, flags=["checked_samples"]),
        ],
    ),
    "frostbite_patient": node(
        "半个人",
        scene_lower,
        55,
        [
            seg("巡检队员睁眼，先叫出你的名字，又叫出连岚妹妹的名字，最后叫出苏小禾妈妈的名字。"),
            seg("“我们不是死人。”他每说一个字，牙齿就碎下一点，“我们是冬天借来的人。”", "巡检队员"),
        ],
        [
            choice("记录他说出的名字", "containment_window", val=1, flags=["recorded_names"], clues=["borrowed_names"]),
            choice("切断床边热源，停止霜丝扩张", "core_bridge", val=4, flags=["cut_patient_heat"], effect="cold"),
        ],
    ),
    "containment_window": node(
        "隔离窗",
        scene_lower,
        57,
        [
            seg("隔离窗后，霜丝在培养皿里组成一张女性的脸。她反复张口，没有声音。"),
            seg("周泠的批注贴在玻璃上：母体并不想杀人。母体想取暖。"),
        ],
        [
            choice("拍下母体形态", "core_bridge", val=1, flags=["saw_mother_shape"], clues=["mother_wants_heat"]),
            choice("用热芯灼烧培养皿，测试反应", "spore_fan", val=5, flags=["tested_spores"], effect="flash"),
        ],
    ),
    "core_bridge": node(
        "核心桥",
        scene_lower,
        59,
        [
            seg("核心桥横跨黑井。桥下传来数百人的呼吸声，整齐、缓慢，像一座城市在睡觉。"),
            seg("桥中央躺着巡检队长卡普尔。他还活着，手里攥着核心钥匙。"),
        ],
        [
            choice("爬到卡普尔身边拿钥匙", "key_panel", val=-2, flags=["approached_kapoor"]),
            choice("先检查桥下呼吸声来源", "coolant_pit", val=1, flags=["looked_under_bridge"]),
        ],
    ),
    "coolant_pit": node(
        "冷却井",
        scene_lower,
        61,
        [
            seg("井下不是水，是成千上万具被霜丝连在一起的身体。他们没有腐烂，像在等待同一个春天。"),
            seg("你看见一名女人抬头。她穿着苏小禾母亲的旧外套。"),
        ],
        [
            choice("向井下喊苏小禾母亲的名字", "nursery_core", val=-3, flags=["called_mother"], clues=["xiaohe_mother_below"]),
            choice("标记井下坐标，继续去核心钥匙台", "key_panel", val=2, flags=["mapped_pit"], clues=["sleeping_city"]),
        ],
    ),
    "spore_fan": node(
        "孢子风扇",
        scene_lower,
        62,
        [
            seg("培养皿受热后爆开，白色孢粉被通风扇卷入管道。警报立刻响起：下层隔离污染。"),
            seg("周泠在通讯里骂了你一句，然后开始手动关闭上行风阀。"),
        ],
        [
            choice("协助周泠关闭上行风阀", "archive_terminal", val=3, flags=["closed_air_valve"], rel={"zhou": 2}),
            choice("放弃风阀，赶去核心钥匙台", "key_panel", val=-4, flags=["spores_in_ducts"], rel={"zhou": -2}),
        ],
    ),
    "key_panel": node(
        "核心钥匙台",
        scene_lower,
        64,
        [
            seg("钥匙台有两个插槽。一个插槽属于热工主管，另一个属于巡检队长。卡普尔的手指已经冻在钥匙柄上。"),
            seg("如果强行掰开，他会醒。或者，某个借他身体说话的东西会醒。"),
        ],
        [
            choice("轻声叫醒卡普尔，要求他自己交出钥匙", "archive_terminal", val=-1, flags=["woke_kapoor"], clues=["kapoor_awake"]),
            choice("切下冻住的手套和钥匙一起带走", "archive_terminal", val=4, flags=["took_core_key"], items=["core_key"], effect="cold"),
        ],
    ),
    "archive_terminal": node(
        "旧档案终端",
        scene_lower,
        66,
        [
            seg("钥匙台旁的旧终端仍在运行。档案标题是：白霜母体供暖共生实验。负责人签名，周泠。"),
            seg("实验目标写得很清楚：让人类在失去太阳后，通过低温共生延长寿命。"),
        ],
        [
            choice("下载完整实验档案", "old_map", val=2, flags=["downloaded_archive"], clues=["coexistence_project"]),
            choice("只复制反应炉控制图，删除实验档案", "old_map", val=-3, flags=["deleted_archive"], clues=["reactor_control_map"]),
        ],
    ),
    "old_map": node(
        "两张地图",
        scene_lower,
        68,
        [
            seg("控制图上有两条管线。红线把热送回居住环，蓝线把热送入冷却井。"),
            seg("如果只走红线，避难站能活。井下会醒来，饥饿地撞向密封门。如果只走蓝线，井下会安静，居住环会失温。"),
        ],
        [
            choice("把两条管线都标记到腕机", "outside_airlock", val=1, flags=["knows_two_pipelines"], clues=["two_pipelines"]),
            choice("优先标记红线，准备救居住环", "generator_room", val=3, flags=["redline_priority"]),
        ],
    ),
    "outside_airlock": node(
        "外部气闸",
        scene_lower,
        70,
        [
            seg("外部气闸通往风暴里的散热塔。塔顶有旧式短波信标，可以呼叫北方车队，但必须有人出站手动点火。"),
            seg("风暴的声音贴在门外，像有很多指甲在同时抓钢板。"),
        ],
        [
            choice("穿防寒服出站点亮信标", "rescue_beacon", val=-6, flags=["lit_beacon"], effect="cold"),
            choice("放弃信标，保留体温去修发电机", "generator_room", val=3, flags=["saved_body_heat"]),
        ],
    ),
    "rescue_beacon": node(
        "风暴信标",
        {
            "id": "storm_tower",
            "name": "散热塔外侧",
            "type": "major",
            "description": "室外白得没有边界，散热塔像一根插在雪原里的黑骨头。",
        },
        72,
        [
            seg("你在风暴里走了二十七步，防寒面罩开始结冰。第十一次呼吸后，你看见雪地里站着许多人影。"),
            seg("他们没有影子，却一起替你挡住风。信标亮起时，你听见苏小禾母亲在你耳边说：别把孩子送下来。"),
        ],
        [
            choice("带着这句话返回下层", "generator_room", val=-3, flags=["heard_mother_warning"], clues=["do_not_send_children"]),
            choice("把信标调成求救和疏散双频", "evacuation_signal", val=-5, flags=["beacon_evac"], clues=["north_convoy"]),
        ],
        ambient="wind",
    ),
    "generator_room": node(
        "辅机室",
        scene_lower,
        73,
        [
            seg("辅机室里的备用发电机还在转，但燃料阀被冻结。只要让它再撑二十分钟，控制室就能远程打开避难站外门。"),
            seg("燃料阀旁边，霜丝像血管一样包住了阀杆。"),
        ],
        [
            choice("用热芯融开燃料阀", "generator_repair", val=4, flags=["used_heat_on_generator"]),
            choice("用破冰锤砸开阀杆", "fuel_choice", val=-2, flags=["hammered_valve"], effect="shake"),
        ],
    ),
    "generator_repair": node(
        "二十分钟",
        scene_lower,
        75,
        [
            seg("发电机重新提速。控制室发来确认：外门可远程开启，但居住环会损失一半热量。"),
            seg("连岚问：“你是要疏散他们，还是把他们锁在这里等你重启？”", "连岚"),
        ],
        [
            choice("准备疏散老人与孩子", "evacuation_signal", val=1, flags=["prepared_evacuation"], rel={"station": 2}),
            choice("保持封闭，所有热量留给核心重启", "fuel_choice", val=5, flags=["kept_station_sealed"], rel={"station": -2}),
        ],
    ),
    "fuel_choice": node(
        "燃料阀后的手",
        scene_lower,
        77,
        [
            seg("阀杆被你转开时，墙内伸出一只霜白的手。它没有抓你，只把一枚生锈的站长徽章放进你掌心。"),
            seg("徽章背面刻着：第一批冻死者，不得进入炉心。"),
        ],
        [
            choice("收起站长徽章", "nursery_core", val=2, flags=["has_station_badge"], clues=["first_dead_ban"], items=["station_badge"]),
            choice("把徽章交给连岚，请她决定是否继续", "nursery_core", val=-1, flags=["lian_has_badge"], rel={"lian": 2}),
        ],
    ),
    "nursery_core": node(
        "霜巢育室",
        scene_nursery,
        80,
        [
            seg("你们终于抵达冷库改造的育室。玻璃后面不是怪物巢穴，而是一排排保温舱。每个舱里都有一个被霜丝包住的人。"),
            seg("苏小禾的母亲站在最里面，胸口开着白色花纹。她看见你，第一句话是：炉子快死了，孩子会冷。"),
        ],
        [
            choice("告诉她苏小禾还活着", "glass_children", val=-2, flags=["told_mother_xiaohe"], rel={"mother": 2}),
            choice("要求她交出巡检队和失踪孩子", "mother_white", val=2, flags=["demanded_people"], rel={"mother": -1}),
        ],
        chapter="第五章：霜巢育室",
        ambient="cold",
    ),
    "glass_children": node(
        "玻璃上的小手",
        scene_nursery,
        82,
        [
            seg("听见苏小禾的名字，玻璃后面所有孢丝同时收缩。几个孩子从雾里显出轮廓，隔着玻璃把手贴上来。"),
            seg("他们没有被吃掉。他们被母体藏在最暖的一层霜里，等着上面的人承认他们还活着。"),
        ],
        [
            choice("承诺打开育室，把孩子带回居住环", "heat_equation", val=-3, flags=["promised_children"], rel={"mother": 2}),
            choice("只要求先释放巡检队，孩子稍后处理", "mother_white", val=1, flags=["prioritized_team"], rel={"mother": -2}),
        ],
    ),
    "mother_white": node(
        "白母",
        scene_nursery,
        84,
        [
            seg("苏小禾的母亲摇头。她身后的霜丝组成许多人的脸，有老人，有孩子，也有连岚妹妹。"),
            seg("“我们没有夺走他们。”她说，“是上面的人先把冷交给我们。现在你们要热，我们也要。”", "白母"),
        ],
        [
            choice("让连岚确认妹妹的身份", "save_lian", val=-2, flags=["let_lian_confirm"], rel={"lian": 2}),
            choice("拒绝谈判，准备焚毁育室", "purge_preparation", val=5, flags=["refused_mother"], effect="flash"),
        ],
    ),
    "heat_equation": node(
        "热量方程",
        scene_nursery,
        86,
        [
            seg("白母给你看她的条件：一半热量给居住环，一半热量给冷却井。她会让孩子回去，也会让井下的死者继续睡。"),
            seg("周泠在通讯里沉默很久，最后说：“理论上可行。代价是供暖效率下降，整个冬季都不会暖，只能不死。”", "周泠"),
        ],
        [
            choice("接受共生方案，准备双线供热", "trial_choice", val=-2, flags=["considered_coexistence"], rel={"mother": 2, "zhou": 1}),
            choice("拒绝牺牲热量，回到核心执行人类优先", "main_core", val=4, flags=["human_priority"]),
        ],
    ),
    "trial_choice": node(
        "试运行",
        scene_nursery,
        88,
        [
            seg("试运行需要有人进入核心井，手动把蓝线阀门保持在半开。阀门会在三分钟内冻结，进去的人很难回来。"),
            seg("连岚看着玻璃后的妹妹，又看向你。周泠说她可以去。白母说她也可以替你们保住一个人。"),
        ],
        [
            choice("自己进入核心井", "main_core", val=3, flags=["player_volunteer"], important=("player_volunteer", "你决定亲自进核心井")),
            choice("接受周泠进入核心井", "main_core", val=1, flags=["zhou_volunteer"], rel={"zhou": 3}, important=("zhou_volunteer", "周泠进入核心井")),
            choice("允许连岚代替你进入核心井", "sacrifice_lian", val=2, flags=["lian_steps_forward"], rel={"lian": 2}),
            choice("让连岚留下陪妹妹，拒绝让她牺牲", "main_core", val=-1, flags=["saved_lian"], rel={"lian": 3}),
        ],
    ),
    "save_lian": node(
        "妹妹",
        scene_nursery,
        89,
        [
            seg("连岚的妹妹从霜丝里睁开眼。她没有扑向姐姐，只问了一句：“上面还有热汤吗？”"),
            seg("连岚放下枪。那一刻，你知道她不会再支持焚毁育室，除非白母先伤害活人。"),
        ],
        [
            choice("让姐妹短暂交谈，争取白母信任", "heat_equation", val=-2, flags=["lian_sister_talk"], rel={"lian": 3, "mother": 1}),
            choice("打断交谈，要求白母立即释放所有人", "purge_preparation", val=3, flags=["broke_reunion"], rel={"lian": -3}),
        ],
    ),
    "sacrifice_lian": node(
        "警卫的选择",
        scene_nursery,
        90,
        [
            seg("连岚把自己的身份牌塞给你。“如果我没回来，把这个给我妹妹。告诉她我没有朝她开枪。”", "连岚"),
            seg("她走向核心井，没有回头。"),
        ],
        [
            choice("带着连岚的身份牌去核心", "main_core", val=2, flags=["lian_sacrificed"], rel={"lian": 5}, items=["lian_badge"]),
        ],
    ),
    "main_core": node(
        "供暖核心",
        scene_core,
        92,
        [
            seg("核心井里热浪和寒雾交替翻滚。控制台给出四个可执行方案：单线重启、双线共生、全站疏散、热焚清除。"),
            seg("每个方案都能让一部分人活下去。没有一个方案干净。"),
        ],
        [
            choice("执行单线重启，只向居住环供热", "manual_restart", val=5, flags=["single_line_restart"], important=("single_line_restart", "你选择人类优先供热")),
            choice("执行双线共生，让居住环和冷却井共享热量", "manual_restart", val=-2, flags=["dual_line_heat"], important=("dual_line_heat", "你选择双线共生")),
            choice("执行热焚清除，烧掉育室和冷却井", "purge_preparation", val=6, flags=["purge_plan"], important=("purge_plan", "你选择热焚清除")),
            choice("启动疏散，把避难站交给风暴", "evacuation_signal", val=-4, flags=["evac_plan"], important=("evac_plan", "你选择全站疏散")),
        ],
        chapter="第六章：核心没有仁慈",
        ambient="heat",
    ),
    "purge_preparation": node(
        "热焚倒计时",
        scene_core,
        94,
        [
            seg("热焚程序需要三十秒预热。育室方向传来孩子们的哭声，也可能只是白霜学会了哭声。"),
            seg("周泠在频道里喊：“如果你按下去，霜丝会死，孩子也会死。你确定他们已经不是人了吗？”", "周泠"),
        ],
        [
            choice("取消热焚，改回核心控制台", "main_core", val=-3, flags=["cancelled_purge"], rel={"zhou": 2}),
            choice("继续热焚，阻止任何白霜上行", "manual_restart", val=5, flags=["confirmed_purge"], effect="flash"),
        ],
    ),
    "evacuation_signal": node(
        "疏散信号",
        scene_core,
        95,
        [
            seg("外门开启指令发出，居住环的广播开始重复：带上热毯，沿北侧坡道撤离。"),
            seg("控制室回传画面里，老人和孩子排成队走进风暴。北方车队的灯还在很远的地方。"),
        ],
        [
            choice("维持疏散，关闭核心井封门", "final_route", val=-2, flags=["evacuation_active"]),
            choice("疏散到一半后反悔，保留部分热量重启核心", "manual_restart", val=2, flags=["partial_evacuation"]),
        ],
    ),
    "manual_restart": node(
        "手动重启",
        scene_core,
        96,
        [
            seg("你把主管钥匙插进控制台。第二个插槽亮起，如果没有巡检队长钥匙，系统会要求活体授权。"),
            seg("核心深处传来很多人的声音，重叠着问你：这次轮到谁取暖？"),
        ],
        [
            choice("插入巡检队长钥匙并执行方案", "final_route", val=2, flags=["used_core_key"]),
            choice("用自己的生命体征替代第二授权", "final_route", val=-6, flags=["used_self_authorization"], important=("self_authorized", "你用自己的生命体征授权")),
        ],
    ),
    "final_route": node(
        "黎明前的判定",
        scene_core,
        98,
        [
            seg("核心开始升温。居住环、育室、冷却井、风暴外门，所有线路同时请求最后确认。"),
            seg("你看见自己的呼吸在控制台前结成白霜。它短暂停留，像一行等待签名的判决。"),
        ],
        routes=[
            {"condition": "hasFlag 'confirmed_purge'", "next": "ending_pyre"},
            {"condition": "hasFlag 'dual_line_heat'", "next": "ending_coexistence"},
            {"condition": "hasFlag 'evacuation_active'", "next": "ending_exile"},
            {"condition": {"all": [{"flag": "single_line_restart"}, {"var": "val", "op": ">=", "value": 62}]}, "next": "ending_dawn"},
            {"condition": "hasFlag 'used_self_authorization'", "next": "ending_core_sleeper"},
            {"condition": "default", "next": "ending_white_city"},
        ],
        ambient="static",
    ),
}

nodes.update(
    {
        "ending_dawn": ending(
            "结局：寒潮后的第一盏灯",
            "TRUE ENDING",
            "单线重启成功。居住环在黎明前恢复供暖，三千名避难者活了下来。下层冷却井被重新封死，井里持续传来敲击声，直到第十三天才停止。",
            "你救下了活着的人，也把另一群学会呼吸的死者继续留在冬天里。春天若还会来，它必须先经过你的签名。",
            "ending_dawn",
            "heat",
        ),
        "ending_coexistence": ending(
            "结局：半暖冬眠",
            "HIDDEN ENDING",
            "双线供热让居住环和冷却井同时稳定。避难站从此再也没有真正暖过，但也没有人在夜里冻死。孩子们陆续醒来，部分第一批冻死者保留了名字和记忆。",
            "人类没有战胜极寒，只是学会和冬天同住一间屋子。每晚九点，你仍要亲自确认蓝线阀门没有开得太大。",
            "ending_coexistence",
            "cold",
        ),
        "ending_pyre": ending(
            "结局：白焰清除",
            "BRANCH ENDING",
            "热焚程序烧穿育室和冷却井。霜丝、白母、孩子和巡检队全部化成蒸汽。居住环得到完整供暖，官方记录称下层污染源已清除。",
            "避难站活了下来，却再没有人敢给孩子讲春天。因为他们知道，有些哭声不是假的，只是被你判定为不够像人。",
            "ending_pyre",
            "blood",
        ),
        "ending_exile": ending(
            "结局：北方灯队",
            "NORMAL ENDING",
            "疏散队伍进入风暴。北方车队在两个小时后接走一千九百人，剩下的人留在雪线后。十七号避难站被白霜吞没，反应炉在无人操作中熄灭。",
            "你带出了一部分活人，也把一座城留给极寒。后来每当车队经过旧址，短波里都会响起儿童合唱般的启动手册。",
            "ending_exile",
            "wind",
        ),
        "ending_core_sleeper": ending(
            "结局：核心守夜人",
            "SPECIAL ENDING",
            "你用自己的生命体征完成授权，核心接受了你。供暖恢复，育室封闭，冷却井安静。你的身体留在控制台旁，体温长期维持在不可能的三十七度。",
            "十七号避难站的人说，供暖主管没有死，只是睡在炉心里。每当温度下降，广播里都会响起你的声音，提醒他们关好门。",
            "ending_core_sleeper",
            "static",
        ),
        "ending_white_city": ending(
            "结局：白城上行",
            "BAD ENDING",
            "核心重启失败，密封门在温差中变形。井下的白霜沿热管上行，先经过医务室，再经过儿童区，最后抵达控制室。避难站没有立刻死亡，它变得很安静。",
            "第七天，北方车队收到十七号避难站的求救信号。信号里有三千个人的声音，同时说这里很暖。",
            "ending_white_city",
            "cold",
        ),
    }
)

CODEX = {
    "clues": {
        "0316": {"label": "03:16 时刻", "description": "巡检队生命体征同时归零的时间，也是多处日志开始互相矛盾的节点。"},
        "borrowed_names": {"label": "借来的姓名", "description": "白霜会借用死者或失踪者的名字，让人误以为熟人还活着。"},
        "child_note": {"label": "苏小禾的纸条", "description": "纸条写着妈妈在炉子下面唱歌，说明孩子们听见的呼唤并不只是幻觉。"},
        "child_song": {"label": "孩子的歌声", "description": "童声从下层管道传来，旋律和启动手册的提示音异常相似。"},
        "children_return": {"label": "孩子正在回来", "description": "感染儿童的体征并非单纯死亡，而是被白霜带入某种低温冬眠。"},
        "coexistence_project": {"label": "共生项目档案", "description": "旧实验曾尝试让白霜与人类共同分配热量，但失败记录被长期封存。"},
        "cold_fever": {"label": "低温高烧", "description": "患者表现为发热症状，却不断主动降温，像身体在制造冬眠环境。"},
        "deleted_warning": {"label": "被删除的警告", "description": "主控日志里被删除的一句话：不要让他们把霜带进热里。"},
        "do_not_restart": {"label": "不要重启", "description": "巡检队留下的警告，暗示反应炉重启会让白霜获得通向居住环的热路。"},
        "do_not_send_children": {"label": "别送孩子上车", "description": "下层记录显示，部分孩子一旦离开供暖核心，体征会迅速崩溃。"},
        "first_dead_ban": {"label": "第一批死者禁令", "description": "早期死亡名单被从公开档案中删去，说明避难站曾隐瞒白霜实验。"},
        "four_minute_gap": {"label": "消失的四分钟", "description": "03:12 到 03:16 之间没有监控画面，却决定了巡检队命运。"},
        "frost_eyes": {"label": "霜中的眼睛", "description": "白霜会在管壁和玻璃上形成类似眼睛的结构，追踪热源与声音。"},
        "frost_teeth": {"label": "霜齿样本", "description": "从白霜结构上取下的硬质样本，像牙，也像某种生长出来的阀门。"},
        "kapoor_awake": {"label": "卡普尔仍醒着", "description": "巡检队员卡普尔没有完全死亡，他可能保留了对白霜母体的记忆。"},
        "kapoor_video": {"label": "卡普尔影像", "description": "影像显示巡检队进入下层后，有人主动关闭了回程门。"},
        "last_locator": {"label": "巡检队最后定位", "description": "巡检队最后一次定位在下层反应炉，随后生命体征同时变成白线。"},
        "mother_under_core": {"label": "炉下的妈妈", "description": "多个孩子都提到炉下有妈妈在唱歌，说明白母正在模仿亲人。"},
        "mother_wants_heat": {"label": "白母需要热量", "description": "白母并不只想杀人，它需要稳定热源维持育室和冬眠者。"},
        "north_convoy": {"label": "北方车队", "description": "北方救援车队仍可能接应一部分幸存者，但风暴会吞掉落后的人。"},
        "old_organ_storage": {"label": "旧器官库", "description": "旧冷库曾用于保存器官和实验体，后来被改造成霜巢育室。"},
        "reactor_control_map": {"label": "反应炉控制图", "description": "控制图标出红线和蓝线两套热路，决定热量流向人群或下层。"},
        "shifting_tags": {"label": "变动的尸袋标签", "description": "尸袋标签在低温中悄悄变换，像有人在重新分配死者身份。"},
        "sleeping_city": {"label": "冬眠城市", "description": "白霜似乎想把整座避难站变成低温冬眠系统，而非立刻杀死所有人。"},
        "speaking_frost": {"label": "会说话的白霜", "description": "白霜能复制熟人的声音，用请求和威胁诱导人打开门或阀门。"},
        "team_sleeve": {"label": "巡检队袖标", "description": "失联队员的袖标出现在不该出现的位置，证明有人或某物移动过他们。"},
        "two_pipelines": {"label": "双管线", "description": "红线向居住环供热，蓝线通往下层冷却井；两条线可以互相牵制。"},
        "white_asks_heat": {"label": "白霜索要热量", "description": "白霜会主动提出交换，说明它理解供暖系统和人的谈判习惯。"},
        "white_mother_drawings": {"label": "白母图纸", "description": "图纸记录白母和供暖核心的连接方式，是共生或清除方案的关键。"},
        "white_roots": {"label": "白色根系", "description": "白霜根系已经长进水培温室和通风管，感染范围比预想更深。"},
        "xiaohe_mother_below": {"label": "小禾母亲在下层", "description": "苏小禾的母亲可能是白母模仿的原型，也是孩子们被召唤的原因。"},
        "zhou_key": {"label": "周泠的钥匙", "description": "周泠保留着旧冷库钥匙，说明她早就知道下层还有被封存的区域。"},
        "zhou_samples": {"label": "周泠样本记录", "description": "样本记录显示周泠一直在追踪感染者的低温变化。"},
    },
    "items": {
        "cold_storage_key": {"label": "旧冷库钥匙", "description": "能打开霜巢育室外层门，也会暴露你已经接近白母。"},
        "core_key": {"label": "核心钥匙", "description": "进入供暖核心手动授权区的钥匙，通常只交给下层巡检队长。"},
        "flare_gun": {"label": "信号枪", "description": "能在风暴中短暂标记位置，也可能吸引外面的东西。"},
        "heat_cell": {"label": "标准热芯", "description": "便携热源，可救人、维持设备，也能引诱白霜靠近。"},
        "lian_badge": {"label": "连岚的肩章", "description": "连岚交给你的身份物，必要时能让警卫队相信你的命令。"},
        "spore_sample": {"label": "白霜孢丝样本", "description": "从白色根系上取下的样本，证明白霜具有生长和模仿能力。"},
        "station_badge": {"label": "旧站牌", "description": "第一批死者留下的身份牌，记录被官方删除的名字。"},
        "tooth_sample": {"label": "霜齿样本", "description": "硬化的白霜碎片，能帮助周泠判断白母是否正在长出新的器官。"},
    },
}

story = {
    "schemaVersion": 2,
    "meta": {
        "title": "白霜七日",
        "author": "Codex 示例",
        "version": "1.0.0",
        "description": "极寒末世中，避难站供暖核心濒临熄火，失联巡检队把一种会模仿人类的白霜带到了炉心下方。",
        "mode": "standard",
        "theme": "horror-house",
        "themePack": "horror-house",
        "prosePreset": "horror-house",
        "playerRole": "十七号避难站热工主管沈砚",
        "objective": "找到失联的供暖核心巡检队，并决定是否重启地下反应炉。",
        "stakes": "如果反应炉在天亮前熄火，三千名避难者会在零下七十度的风暴里冻死。",
        "mechanics": ["clues", "inventory", "relationship", "timePressure"],
        "decisionPacing": {"windowSize": 10, "maxDecisionPages": 5, "maxConsecutiveDecisionPages": 2},
        "themePackData": {
            "visual": {
                "palette": ["#07090d", "#121923", "#1f2b36", "#edf7ff", "#8fd3ff", "#d66b63"],
                "background": "polar night, frost on glass, emergency red lamps",
                "surface": "dark insulated panels, thin ice-blue borders",
                "button": "hard-edged survival console choices",
                "transition": "cold cuts, static, breath fade",
            },
            "typography": {
                "heading": "ui-sans-serif, system-ui, sans-serif",
                "body": "ui-serif, Georgia, serif",
                "voice": "clear survival horror",
            },
            "prose": {
                "preset": "horror-house",
                "sentenceLength": "mixed",
                "dialogue": "direct under pressure",
                "avoid": ["pure atmosphere", "unclear monster rules", "abstract choice labels"],
            },
            "launcher": {
                "layout": "reader-with-side-panel",
                "status": ["bodyHeat", "flags", "clues", "items"],
                "choiceStyle": "compact-list",
                "sceneTransition": "cold-cut",
            },
        },
        "cover": {
            "label": "WHITEOUT / DAY 7",
            "tagline": "供暖核心还剩六小时。不要回答会说话的死人。",
        },
        "variableName": "体温",
        "initialVariable": 58,
    },
    "startNodeId": "start",
    "variables": {"time": 0, "storm": "whiteout", "stationPopulation": 3000},
    "achievements": {
        "first_descent": {"title": "第一次下行", "description": "离开控制室，开始寻找巡检队。"},
        "truth_archive": {"title": "共生档案", "description": "找到白霜母体实验档案。"},
        "child_note": {"title": "妈妈在炉下", "description": "取得苏小禾的纸条或录音线索。"},
        "storm_beacon": {"title": "风暴信标", "description": "在室外点亮散热塔短波信标。"},
        "white_mother": {"title": "白母", "description": "见到霜巢育室中的母体。"},
        "ending_dawn": {"title": "寒潮后的第一盏灯", "description": "让居住环恢复供暖。"},
        "ending_coexistence": {"title": "半暖冬眠", "description": "达成双线共生。"},
        "ending_pyre": {"title": "白焰清除", "description": "执行热焚清除。"},
        "ending_exile": {"title": "北方灯队", "description": "启动全站疏散。"},
        "ending_core_sleeper": {"title": "核心守夜人", "description": "用自己的生命体征完成授权。"},
        "ending_white_city": {"title": "白城上行", "description": "让白霜抵达居住环。"},
    },
    "codex": CODEX,
    "nodes": nodes,
}

nodes["choose_route"]["choices"][0]["changes"]["unlockAchievement"] = "first_descent"
nodes["choose_route"]["choices"][1]["changes"]["unlockAchievement"] = "first_descent"
nodes["choose_route"]["choices"][2]["changes"]["unlockAchievement"] = "first_descent"
nodes["patient_xiaohe"]["choices"][0]["changes"]["unlockAchievement"] = "child_note"
nodes["dorm_recording"]["choices"][0]["changes"]["unlockAchievement"] = "child_note"
nodes["archive_terminal"]["choices"][0]["changes"]["unlockAchievement"] = "truth_archive"
nodes["rescue_beacon"]["choices"][0]["changes"]["unlockAchievement"] = "storm_beacon"
nodes["nursery_core"]["choices"][0]["changes"]["unlockAchievement"] = "white_mother"
nodes["nursery_core"]["choices"][1]["changes"]["unlockAchievement"] = "white_mother"

Path(__file__).with_name("story.json").write_text(
    json.dumps(story, ensure_ascii=False, indent=2), encoding="utf-8"
)
