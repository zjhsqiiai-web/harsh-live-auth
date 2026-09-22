import discord
import asyncio
import os
import time
import random 
import re
import logging
from keep_alive import keep_alive

# 🔥 INJECT THE HYPER-ENGINE HERE
import sys
if sys.platform != "win32":
    try:
        import uvloop
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        print("🚀 [SYSTEM] UVLOOP ENGINE ENGAGED. MAXIMUM SPEED UNLOCKED.")
    except ImportError:
        print("⚠️ [SYSTEM] uvloop package not installed. Continuing with standard event loop.")

# 1. TURN ON DISCORD X-RAY (Keeps your general boot-up info flowing)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(name)s: %(message)s')

# 2. 🛑 THE GAG ORDER: Mutes the specific HTTP rate limit spam
logging.getLogger('discord.http').setLevel(logging.ERROR)

# 3. SMART LOG MATRIX TIMER (For your custom loops)
global_last_log = 0

# 🟢 THE SWARM REGISTRY: Tracks breathing tokens in real-time
ACTIVE_SWARM = []
# 🟢 THE SLIDE REGISTRY: Tracks users to relentlessly roast on sight
SLIDE_TARGETS = set()
# 🟢 SMART SPAM REGISTRY: Maps target user IDs to your custom text
SSPAM_TARGETS = {}
# 🟢 SMART GCNC REGISTRY: Maps target user IDs to custom GC name text
SGCNC_TARGETS = {}
# 🟢 GLOBAL COMMAND DISPATCH REGISTRY
GLOBAL_GCNC_ALL_TASKS = {}

# 2. Extract configuration constants
PREFIX = "^"
MAIN_OWNER = 1546429341775171585
AUTHORIZED_USERS = []
# ⚡ FAST BOOT TOGGLE: 
# Set to TRUE for instant local testing (1s delay).
# Set to FALSE when deploying to Railway for full security cloak (15s+ delay).
FAST_BOOT = True
# 🔥 GLOBAL BROWSER HEADERS (Bypasses Cloudflare IP blocks)
BROWSER_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "Sec-Ch-Ua-Mobile": "?2",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Connection": "keep-alive"
}

# Global dictionaries to track active tasks across all clients
gcnc_tasks = {}
spam_tasks = {}
active_monitors = {}

class ForbidToken(discord.Client):
    def __init__(self, *args, **kwargs):
        # 1. No intents needed for discord.py-self, just initialize directly
        super().__init__(*args, **kwargs)
        self.raw_session = None  # This will hold our high-speed socket
        self.processed_sspam_ids = set()  # 🟢 PREVENTS A SINGLE BOT FROM FIRING TWICE ON THE SAME MESSAGE

    # 🛑 ADD THIS RIGHT AT THE TOP OF YOUR CLASS
    async def on_ready(self):
        import aiohttp
        print(f"🟢 [{self.user.name}] Self-Bot Account Operational.", flush=True)
        
        # 🟢 HEALTH MONITOR: Bot registers itself as ALIVE
        if getattr(self.user, 'id', None) not in ACTIVE_SWARM:
            ACTIVE_SWARM.append(self.user.id)
            print(f"📊 [System] Swarm Capacity updated: {len(ACTIVE_SWARM)} Nodes Active.", flush=True)

        # 🚀 ULTRA-ACCELERATED TCP POOL: Uncapped connection reuse for maximum velocity
        connector = aiohttp.TCPConnector(
            limit=None,
            limit_per_host=0,
            enable_cleanup_closed=True,
            force_close=False,
            use_dns_cache=True
        )

        self.raw_session = aiohttp.ClientSession(
            connector=connector,
            headers={
                "Authorization": self.http.token,
                "Content-Type": "application/json",
                "Connection": "keep-alive"
            }
        )
        self.loop.create_task(self.ram_cleaner_loop())
        # 🔥 MOVE IT HERE: Starts safely once the event loop is running
        self.loop.create_task(self.immortal_presence_loop())

    async def immortal_presence_loop(self):
        await self.wait_until_ready()
        while not self.is_closed():
            try:
                # Forces an active session fingerprint so Discord never idles you
                await self.change_presence(
                    status=discord.Status.online,
                    afk=False,
                    activity=discord.Streaming(name="FORB1D NETWORK // ONLINE", url="https://www.twitch.tv/forb1d")
                )
            except Exception:
                pass
            await asyncio.sleep(45)  # Refreshes faster to lock the socket session

    # 🛑 ADD THIS RIGHT UNDER ON_READY
    async def on_disconnect(self):
        # 🛑 HEALTH MONITOR: Bot registers itself as DEAD and forces math recalculation
        if self.user.id in ACTIVE_SWARM:
            ACTIVE_SWARM.remove(self.user.id)
            print(f"⚠️ [System] {self.user.name} dropped connection! Swarm auto-healed to {len(ACTIVE_SWARM)} Nodes.", flush=True)
                
    
    async def on_message(self, message):
        # 1. Bot ignores its own messages to prevent infinite loops
        if message.author == self.user:
            return

        # =========================================================
        # ⚡ ATOMIC SMART GCNC MIRROR ENGINE (ZERO LAG / NO LOOPS) ⚡
        # =========================================================
        if isinstance(message.channel, discord.GroupChannel) and message.type == discord.MessageType.channel_name_change:
            if message.author.id in SGCNC_TARGETS:
                async def atomic_gcnc_override():
                    try:
                        import orjson
                        base_name = SGCNC_TARGETS[message.author.id]
                        
                        # Elite template array with clean symbols
                        templates = [
                            f"⚡ 𝗙𝗢𝗥𝗕𝟭𝗗 𝗞𝗜𝗡𝗚 【 {base_name} 】 ﷽﷽﷽",
                            f"👑 ＦＯＲＢ１Ｄ ＫＩ𝗡Ｇ ꧅ {base_name} ꧅ 𒐫𒐫𒐫",
                            f"☠️ 𝐅𝐎𝐑𝐁𝟏𝐃 𝐊𝐈𝐍𝐆 ╳ {base_name} ╳ 𒈙𒈙𒈙"
                        ]
                        
                        # 200 IQ Swarm Coordination: Pick one primary active node to execute instantly 
                        # to avoid race conditions and double-triggers
                        current_swarm_size = max(1, len(ACTIVE_SWARM))
                        try:
                            my_math_id = ACTIVE_SWARM.index(self.user.id)
                        except ValueError:
                            my_math_id = 0
                            
                        # Micro-stagger based on swarm position to guarantee zero 429 collisions
                        await asyncio.sleep(my_math_id * 0.03)
                        
                        # Select template deterministically based on message ID hash
                        chosen_template = templates[message.id % len(templates)]
                        if len(chosen_template) > 100:
                            chosen_template = chosen_template[:100]
                            
                        target_url = f"https://discord.com/api/v9/channels/{message.channel.id}/messages"
                    
                        # Merge token with global browser headers
                        ultra_headers = BROWSER_HEADERS.copy()
                        ultra_headers["Authorization"] = self.http.token
                        raw_packet = orjson.dumps({"name": chosen_template})
                        
                        async with self.raw_session.patch(target_url, data=raw_packet, headers=ultra_headers) as resp:
                            if resp.status == 429:
                                rate_data = orjson.loads(await resp.read())
                                await asyncio.sleep(rate_data.get("retry_after", 0.5))
                                await self.raw_session.patch(target_url, data=raw_packet, headers=ultra_headers)
                    except Exception:
                        pass
                
                asyncio.create_task(atomic_gcnc_override())
        # =========================================================

        # =========================================================
        # ⚡ ULTIMATE PC & MOBILE OPTIMIZED SMART SPAM ENGINE ⚡
        # =========================================================
        author_id_int = message.author.id
        author_id_str = str(author_id_int)
        
        active_target_text = None
        if author_id_int in SSPAM_TARGETS:
            active_target_text = SSPAM_TARGETS[author_id_int]
        elif author_id_str in SSPAM_TARGETS:
            active_target_text = SSPAM_TARGETS[author_id_str]

        if active_target_text and message.author != self.user:
            # 🛑 SERVER GUARD: Strictly block sspam in any server/guild (Only allow DMs & Group Chats)
            if message.guild is not None:
                return

        if active_target_text and message.author != self.user:
            # 🛑 INSTANT DEDUPLICATION: Prevents a single bot from double-firing on the same message ID
            if message.id in self.processed_sspam_ids:
                return
            self.processed_sspam_ids.add(message.id)
            
            if len(self.processed_sspam_ids) > 500:
                self.processed_sspam_ids.pop()

            async def trigger_stunning_mobile_pc_spam():
                try:
                    import orjson
                    
                    # 🔥 LETHAL HATER EMOJI POOL
                    emojis = ["💀", "👑", "⚡", "🔥", "🔪", "🗡️", "⚔️", "🩸", "☠️", "🔱"]
                    chosen_emoji = emojis[message.id % len(emojis)]
                    
                    # 🔥 CLEAN, HARD-HITTING TITLES (Zero AI fluff)
                    stunning_templates = [
                        "👑 **𝙁𝙊𝙍𝘽1𝘿  //  𝗧𝗛𝗘  𝗞𝗜𝗡𝗚**\n> ⚡ `{user_text} ({emoji})` ➔ <@{target_id}>",
                        "⚡ **𝙁𝙊𝙍𝘽1𝘿  //  𝗢𝗩𝗘𝗥𝗟𝗢𝗥𝗗**\n> ☠️ `{user_text} ({emoji})` ➔ <@{target_id}>",
                        "🔥 **𝙁𝙊𝙍𝘽1𝘿  //  𝗦𝗨𝗣𝗥𝗘𝗠𝗘**\n> 👑 `{user_text} ({emoji})` ➔ <@{target_id}>"
                    ]
                    
                    # Select template deterministically based on message snowflake
                    raw_template = stunning_templates[message.id % len(stunning_templates)]
                    base_content = raw_template.replace("{user_text}", active_target_text).replace("{emoji}", chosen_emoji).replace("{target_id}", str(message.author.id))
                    
                    # Scale it up cleanly to flood the chat window with maximum velocity
                    spaced_content = base_content.replace(" ", " \u200B")
                    block_length = len(spaced_content) + 2
                    multiplier = 1950 // block_length
                    if multiplier < 1: multiplier = 1
                    
                    final_content = "\n\n".join([spaced_content] * multiplier)
                    raw_packet = orjson.dumps({"content": final_content})
                    
                    target_url = f"https://discord.com/api/v9/channels/{message.channel.id}/messages"
                    
                    # Merge token with global browser headers
                    ultra_headers = BROWSER_HEADERS.copy()
                    ultra_headers["Authorization"] = self.http.token
                    
                    # 🔥 FIRE INSTANTLY AT MAXIMUM RUST SPEED VIA KEEP-ALIVE SOCKET POOL
                    async with self.raw_session.post(target_url, data=raw_packet, headers=ultra_headers) as resp:
                        if resp.status == 429:
                            rate_data = orjson.loads(await resp.read())
                            retry_after = float(rate_data.get("retry_after", 0.3))
                            await asyncio.sleep(retry_after)
                            async with self.raw_session.post(target_url, data=raw_packet, headers=ultra_headers):
                                pass
                        elif resp.status not in (200, 201):
                            print(f"⚠️ [SSPAM Error] Status: {resp.status}", flush=True)
                            
                except Exception as e:
                    print(f"⚠️ [SSPAM Critical Exception]: {e}", flush=True)
            
            asyncio.create_task(trigger_stunning_mobile_pc_spam())
        

        # =========================================================
        # 🎯 THE SLIDE ENGINE (MUST BE AT THE VERY TOP) 🎯
        # =========================================================
        if message.author.id in SLIDE_TARGETS:
            async def apply_slide_roast():
                try:
                    my_math_id = self.user.id % 8
                    await asyncio.sleep((my_math_id * 0.05) + random.uniform(0.01, 0.03))
                    
                    slide_roasts = [
                        f"ƒ✿rʙÏd Aʙʙu ＄㉫ ʙħÏdéＧA?!?  çђāl ţęŗj åm̊m̊å x̊o̊d̊t̊å <@{message.author.id}> 💀",
                        f"FФЯБID ИΞ ΓΞЯI MД CФD DI  ƒσɾɓίδ ႪႩႩႲ ♭✺ℓ <@{message.author.id}> 🔥",
                        f"ᵒʸᵉ fσявι∂ кι gυℓαмι кя яи∂у¢є  †℮ґѦ ∂ℌ¥Ѧη  ꀘꍏꀍꍏ ꀍ ţęŗā ƒoŗbįd ābbų  ƴAħA ħ <@{message.author.id}> 🤡",
                        f"ᠻꪮ𝘳᥇𝓲ᦔ 𝘴ꫀ ᵇʰⁱᵈᵉᵍᵃ? 🅘︎🅣︎🅝︎🅘︎ 🅐︎🅤︎🅚︎🅐︎🅣︎? ᵗᵉʳⁱ ᵇʰᵉⁿ ᵏᵒ 𝚛𝚘𝚊𝚍 𝚙𝚎 𝚌𝚘𝚍𝚞 <@{message.author.id}> ⚡",
                        f"chαl вє ᑕᑌᗪKᗪ †℮ґѦ Ѧ♭♭ʊ ƒ◎ґ♭ї∂ ѦℊѦ¥𐌡 𝖙𝖊𝖗𝖎 𝖒𝖆 𝖓𝖊 𝖈𝖚dк𝖉 ѕuícídє ҜЯLIД <@{message.author.id}> ☠️",
                        f"ςђคใ вє ƒ✿rʙÏd †℮ґї ѦммѦ кѦ ґ℮℘ kRǸЄ ﻝArA <@{message.author.id}> 🔱",
                        f"ƒ◎ґ♭ї∂ ℘Ѧ℘Ѧ s̊e̊ b̊h̊åẘ lპႺႩ? ჶ  †℮ґї мѦ LUΠD ℘ḙ <@{message.author.id}> 💥",
                        f"σує FФЯБID ҜI GЦLДMI кѦґ ℊґї♭   ᥴꫝꪊᦔ𝘬ᦔ 𝘬𝓲 ꪖꪊꪶꪶꪖᦔ <@{message.author.id}> 👑",
                        f"ҒΩRβID TΣRΔ ΔββU ѦℊѦʏѦ †℮ґї n̊ån̊i̊ ɕհσδηε ႺႪ RტႩმ pāŗ <@{message.author.id}> 🔥"
                    ]
                    await message.reply(random.choice(slide_roasts), mention_author=True)
                except Exception:
                    pass
            
            asyncio.create_task(apply_slide_roast())
        # =========================================================

        # =========================================================
        # 🟢 THE AUTO-REACT ENGINE
        # =========================================================
        global AUTO_REACT_TARGETS
        if "AUTO_REACT_TARGETS" not in globals():
            AUTO_REACT_TARGETS = {}

        if message.author.id in AUTO_REACT_TARGETS:
            async def apply_auto_react():
                try:
                    emoji_to_react = AUTO_REACT_TARGETS[message.author.id]
                    my_math_id = self.user.id % 8
                    await asyncio.sleep((my_math_id * 0.15) + random.uniform(0.01, 0.05))
                    await message.add_reaction(emoji_to_react)
                except Exception:
                    pass
            asyncio.create_task(apply_auto_react())

        # 1. PREFIX CHECK: Must start with prefix to be treated as a command
        if not message.content.startswith(PREFIX):
            return

        parts = message.content[len(PREFIX):].split()
        if not parts: 
            return
            
        command = parts[0].lower()

        

        # 2. SECURITY WALL & SWARM ROAST ENGINE FOR UNAUTHORIZED USERS
        if message.author.id != MAIN_OWNER and message.author.id not in AUTHORIZED_USERS:
            async def swarm_roast():
                try:
                    # Zipper stagger so all active bots roast cleanly without hitting rate limits
                    my_math_id = self.user.id % 8
                    await asyncio.sleep((my_math_id * 0.15) + random.uniform(0.01, 0.05))
                    
                    roasts = [
                        f"Nice try, <@{message.author.id}>. You don't have the keys to Forbid Bots whip. 💀",
                        f"Bro really thought he could use FORB1D's Bot commands. Stay down, <@{message.author.id}>. 😂",
                        f"Access denied, <@{message.author.id}>. Go make your own script instead of using Forbid Bot kiddo. 🤡",
                        f"Who let this random <@{message.author.id}> try to run Forbid Bot commands? Get lost. ☠️"
                    ]
                    await message.channel.send(random.choice(roasts))
                except Exception as e:
                    print(f"⚠️ Swarm roast failed for {self.user.name}: {e}", flush=True)

            asyncio.create_task(swarm_roast())
            return

        # Clean logging: Only prints to Render when an actual authorized command is given
        print(f"⚡ [{self.user.name}] executing '{command}' for {message.author.name}", flush=True)
        # 4. Your Commands!
        # (We will paste ping here next)
        
                

        if command == "ping":
            if not isinstance(message.channel, discord.DMChannel):
                try: await message.delete()
                except: pass

            # Private memory for each alt so they don't overwrite each other
            if not hasattr(self, 'active_monitors'):
                self.active_monitors = {}
            if not hasattr(self, 'active_ping_tasks'):
                self.active_ping_tasks = {}

            msg = await message.channel.send("`[!] FORB1D🔥 // INITIALIZING...`")
            self.active_monitors[message.channel.id] = msg
            
            # The background thread so the bot doesn't freeze and can hear unping
            async def ping_loop(channel_id, target_msg):
                try:
                    while hasattr(self, 'active_monitors') and self.active_monitors.get(channel_id) == target_msg:
                        latency = round(self.latency * 1000)
                        status_emoji = "🟢" if latency < 50 else "🟡" if latency < 150 else "🔴"
                        status_text = "OPTIMAL" if latency < 50 else "STABLE" if latency < 150 else "LAGGY"
                        
                        await target_msg.edit(content=
                            f"**FORB1D🔥 // SYSTEM PANEL**\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"⚡ **GATEWAY:** `{latency}ms`\n"
                            f"{status_emoji} **STATUS:** `{status_text}`\n"
                            f"🛠️ **INTERFACE:** `ACTIVE`\n"
                            f"━━━━━━━━━━━━━━━━━━━━━━\n"
                            f"Use `{PREFIX}unping` to terminate."
                        )
                        await asyncio.sleep(random.uniform(4.5, 5.5))
                except: 
                    if hasattr(self, 'active_monitors') and channel_id in self.active_monitors: 
                        del self.active_monitors[channel_id]

            # Fire off the task
            task = asyncio.create_task(ping_loop(message.channel.id, msg))
            self.active_ping_tasks[message.channel.id] = task

        elif command == "unping":
            if not isinstance(message.channel, discord.DMChannel):
                try: await message.delete()
                except: pass

            if hasattr(self, 'active_monitors') and message.channel.id in self.active_monitors:
                msg = self.active_monitors.pop(message.channel.id)
                
                # Kill the background loop instantly
                if hasattr(self, 'active_ping_tasks') and message.channel.id in self.active_ping_tasks:
                    task = self.active_ping_tasks.pop(message.channel.id)
                    task.cancel()

                try:
                    await msg.edit(content="`[!] FORB1D🔥 // SHUTTING DOWN...`")
                    await asyncio.sleep(1.5)
                    await msg.delete()
                except:
                    pass

        elif command == "gccall":
            if not isinstance(message.channel, discord.GroupChannel):
                return await message.channel.send(f"❌ **{self.user.name}** Error: This command only works inside Group Chats.")

            task_name = f"gccall_{message.channel.id}"
            for task in asyncio.all_tasks():
                if task.get_name() == task_name and not task.done():
                    return await message.channel.send(f"⚠️ **{self.user.name}** Group call spam is already active in this GC.")

            # 🔥 CYBERPUNK MISSED-CALL ASSAULT NOTIFICATION
            await message.channel.send(
                f"⚡ **[ FORB1D MISSED-CALL ASSAULT ]** ⚡\n"
                f"> 📞 Target: `GROUP CHAT`\n"
                f"> 🩸 Status: `2-SEC RING & DROP LOOP ENGAGED...`\n"
                f"> 💀 Node: **{self.user.name}**"
            )

            async def gateway_call_loop():
                # 🟢 SWARM MATHEMATICAL STAGGER: Prevents collision when 4+ bots run simultaneously
                current_swarm_size = max(1, len(ACTIVE_SWARM))
                try:
                    my_math_id = ACTIVE_SWARM.index(self.user.id)
                except ValueError:
                    my_math_id = self.user.id % current_swarm_size

                # Initial offset so bots enter the loop sequentially
                await asyncio.sleep(my_math_id * 0.4)

                while True:
                    try:
                        # Step 1: Join/Ring Signal (Opcode 4)
                        payload = {
                            "op": 4,
                            "d": {
                                "guild_id": None,
                                "channel_id": str(message.channel.id),
                                "self_mute": True,
                                "self_deaf": True,
                                "self_video": False
                            }
                        }
                        
                        if self.ws and self.ws.open:
                            await self.ws.send_as_json(payload)
                        
                        # ⏱️ Stay connected for EXACTLY 2 seconds to initiate the ring tone
                        await asyncio.sleep(2.0)
                        
                        # Step 2: Full Leave/Drop Signal (Triggers the "Missed Call" chat bubble popup)
                        drop_payload = {
                            "op": 4,
                            "d": {
                                "guild_id": None,
                                "channel_id": None,
                                "self_mute": True,
                                "self_deaf": True,
                                "self_video": False
                            }
                        }
                        if self.ws and self.ws.open:
                            await self.ws.send_as_json(drop_payload)
                            
                        # ⏱️ Cooldown delay so Discord registers the drop and allows the missed call notification to render
                        await asyncio.sleep(1.5 + (my_math_id * 0.1))
                    except Exception:
                        await asyncio.sleep(2.0)

            task = asyncio.create_task(gateway_call_loop(), name=task_name)
            if message.channel.id not in gcnc_tasks:
                gcnc_tasks[message.channel.id] = []
            gcnc_tasks[message.channel.id].append(task)

        elif command == "ungccall":
            task_name = f"gccall_{message.channel.id}"
            killed = False
            for task in asyncio.all_tasks():
                if task.get_name() == task_name:
                    task.cancel()
                    killed = True

            try:
                drop_payload = {
                    "op": 4,
                    "d": {
                        "guild_id": None,
                        "channel_id": None,
                        "self_mute": True,
                        "self_deaf": True,
                        "self_video": False
                    }
                }
                if self.ws and self.ws.open:
                    await self.ws.send_as_json(drop_payload)
            except Exception:
                pass

            await asyncio.sleep(self.user.id % 8 * 0.2)
            if killed:
                await message.channel.send(
                    f"🛑 **[ FORB1D AUDIO ASSAULT TERMINATED ]** 🛑\n"
                    f"> 💤 Status: `GATEWAY ROUTER DISENGAGED`\n"
                    f"> 💀 Node: **{self.user.name}**"
                )
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active GC call loop running here.")

        elif command == "reset":
            # 🛑 LOCK: Restrict reset access to owner/authorized users
            if message.author.id != MAIN_OWNER and message.author.id not in AUTHORIZED_USERS:
                return await message.channel.send(f"❌ **{self.user.name}** Access Denied: You cannot reset the network.")

            # Send the initial cyberpunk-themed progress tracker message
            progress_msg = await message.channel.send(
                f"⚡ **[ FORB1D CORE OVERRIDE ]** ⚡\n"
                f"> 🔌 Status: `INITIALIZING SYSTEM PURGE...`\n"
                f"> 📊 Progress: `[▒▒▒▒▒▒▒▒▒▒] 0%`"
            )

            try:
                # Step 1: Wipe all global task dictionaries, hater registries, and target maps (25%)
                await asyncio.sleep(0.25)
                spam_tasks.clear()
                gcnc_tasks.clear()
                SLIDE_TARGETS.clear()
                SSPAM_TARGETS.clear()
                SGCNC_TARGETS.clear()
                ACTIVE_SWARM.clear()
                
                await progress_msg.edit(content=
                    f"⚡ **[ FORB1D CORE OVERRIDE ]** ⚡\n"
                    f"> 🔌 Status: `FLUSHING MEMORY REGISTRIES...`\n"
                    f"> 📊 Progress: `[███▒▒▒▒▒▒▒] 25%`"
                )

                # Step 2: Cancel all background tracking/spam/flasher tasks across the loop (50%)
                await asyncio.sleep(0.25)
                cancelled_count = 0
                for task in asyncio.all_tasks():
                    if task != asyncio.current_task() and not task.done():
                        task_name = task.get_name()
                        if any(x in task_name for x in ["spam_", "gcnc_", "forward_", "gcspamall_", "gcncall_"]):
                            task.cancel()
                            cancelled_count += 1
                
                await progress_msg.edit(content=
                    f"⚡ **[ FORB1D CORE OVERRIDE ]** ⚡\n"
                    f"> 🔌 Status: `TERMINATING {cancelled_count} ZOMBIE THREADS...`\n"
                    f"> 📊 Progress: `[██████▒▒▒▒] 50%`"
                )

                # Step 3: Run deep garbage collection to clear out memory fragments (75%)
                await asyncio.sleep(0.25)
                import gc
                collected = gc.collect()
                
                await progress_msg.edit(content=
                    f"⚡ **[ FORB1D CORE OVERRIDE ]** ⚡\n"
                    f"> 🔌 Status: `PURGING {collected} FRAGMENTED OBJECTS...`\n"
                    f"> 📊 Progress: `[█████████▒] 75%`"
                )

                # Step 4: Re-register current bot into the active swarm safely (100%)
                await asyncio.sleep(0.3)
                if self.user.id not in ACTIVE_SWARM:
                    ACTIVE_SWARM.append(self.user.id)

                await progress_msg.edit(content=
                    f"⚡ **[ FORB1D CORE OVERRIDE ]** ⚡\n"
                    f"> 🔌 Status: `SYSTEMS RESTORED // ALL NODES GREEN`\n"
                    f"> 📊 Progress: `[██████████] 100%`\n"
                    f"✨ **SUCCESS: Network fully cleansed and operational!**"
                )

                print(f"🔄 [{self.user.name}] Cyberpunk In-Memory Reset complete. All systems normal.", flush=True)

            except Exception as e:
                print(f"❌ [Reset Error]: {e}", flush=True)
                await message.channel.send(f"❌ Reset failed: {e}")

        elif command == "gcspamall":
            # Usage: ^gcspamall <text>
            if len(parts) < 2:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^gcspamall <text>`")
            
            user_text = " ".join(parts[1:])
            
            async def global_gc_spam_loop():
                # Grab every single Group Chat this specific bot token is currently inside
                target_gcs = [ch for ch in self.private_channels if isinstance(ch, discord.GroupChannel)]
                
                if not target_gcs:
                    print(f"⚠️ [{self.user.name}] No Group Chats found for global spam.", flush=True)
                    return

                print(f"🚀 [{self.user.name}] Starting global spam across {len(target_gcs)} GCs...", flush=True)
                
                emojis = ["💀", "👑", "⚡", "🔥", "☠️"]
                idx = self.user.id % len(emojis)
                
                while True:
                    try:
                        chosen_emoji = emojis[idx]
                        idx = (idx + 1) % len(emojis)
                        
                        base_text = f"👑 **𝙁𝙊𝙍𝘽1𝘿 // 𝗧𝗛𝗘 𝗞𝗜𝗡𝗚**\n> ⚡ `{user_text} ({chosen_emoji})`"
                        spaced_content = base_text.replace(" ", " \u200B")
                        
                        multiplier = 1950 // (len(spaced_content) + 2)
                        if multiplier < 1: multiplier = 1
                        final_content = "\n\n".join([spaced_content] * multiplier)
                        
                        import orjson
                        raw_packet = orjson.dumps({"content": final_content})
                        
                        # Loop through each GC with a built-in micro-delay to prevent global rate-limit chains (429)
                        for gc in target_gcs:
                            try:
                                target_url = f"https://discord.com/api/v9/channels/{gc.id}/messages"
                                ultra_headers = BROWSER_HEADERS.copy()
                                ultra_headers["Authorization"] = self.http.token
                                
                                async with self.raw_session.post(target_url, data=raw_packet, headers=ultra_headers) as resp:
                                    if resp.status == 429:
                                        rate_data = orjson.loads(await resp.read())
                                        retry_after = float(rate_data.get("retry_after", 1.0))
                                        await asyncio.sleep(retry_after)
                                        async with self.raw_session.post(target_url, data=raw_packet, headers=ultra_headers):
                                            pass
                                # Snip-delay between individual GC endpoints to keep safety high
                                await asyncio.sleep(0.4)
                            except Exception:
                                pass
                                
                        # Delay before next full loop cycle across all GCs
                        await asyncio.sleep(3.0)
                        
                    except Exception as e:
                        print(f"⚠️ [Global GC Spam Error]: {e}", flush=True)
                        await asyncio.sleep(1.0)

            task = asyncio.create_task(global_gc_spam_loop(), name=f"gcspamall_{self.user.id}")
            if message.channel.id not in spam_tasks:
                spam_tasks[message.channel.id] = []
            spam_tasks[message.channel.id].append(task)
            
            if self.user.id % 8 == 0 or self.user.id % 8 == 1:
                await message.channel.send(f"✅ FORB1D🔥 **Global GC Spam** initiated across all available channels.")

        elif command == "ungcspamall":
            killed_count = 0
            
            # Search and cancel all global gcspamall tasks across the entire event loop
            for task in asyncio.all_tasks():
                if task.get_name().startswith("gcspamall_"):
                    task.cancel()
                    killed_count += 1
            
            await asyncio.sleep(self.user.id % 8 * 0.2)
            if killed_count > 0:
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated global GC spam loops across the network.")
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active global GC spam running.")

        elif command == "gcncall":
            if len(parts) < 2:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^gcncall <text>` or `^gcncall stop`")
            
            if parts[1].lower() == "stop":
                killed = False
                for task in asyncio.all_tasks():
                    if task.get_name() == f"gcncall_{self.user.id}":
                        task.cancel()
                        killed = True
                
                await asyncio.sleep(self.user.id % 8 * 0.2)
                if killed:
                    return await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated global GC name flasher loops.")
                else:
                    return await message.channel.send(f"⚠️ **{self.user.name}** found no active global GC name flasher running.")

            base_name = " ".join(parts[1:])
            
            async def math_global_gcnc_loop():
                # 🔥 CYCLING EMOJI POOL FOR MAXIMUM VISUAL SPEED & CHAOS
                emojis = ["💀", "👑", "⚡", "🔥", "☠️", "🔱", "💎", "💥"]
                
                import orjson
                while True:
                    try:
                        # Grab every GC this specific token instance is inside
                        target_gcs = [ch for ch in self.private_channels if isinstance(ch, discord.GroupChannel)]
                        if not target_gcs:
                            await asyncio.sleep(2.0)
                            continue

                        current_swarm_size = max(1, len(ACTIVE_SWARM))
                        try:
                            my_math_id = ACTIVE_SWARM.index(self.user.id)
                        except ValueError:
                            my_math_id = self.user.id % current_swarm_size

                        for index, gc in enumerate(target_gcs):
                            try:
                                emoji_index = (index + int(time.time())) % len(emojis)
                                chosen_emoji = emojis[emoji_index]

                                exact_template = f"{chosen_emoji} 𝗙𝗢𝗥𝗕𝟭𝗗 𝗞𝗜𝗡𝗚 【 {base_name} 】 {chosen_emoji} ﷽﷽"
                                if len(exact_template) > 100:
                                    exact_template = exact_template[:100]

                                raw_packet = orjson.dumps({"name": exact_template})

                                channel_stagger = ((index + my_math_id) % current_swarm_size) * 0.05
                                await asyncio.sleep(channel_stagger)

                                target_url = f"https://discord.com/api/v9/channels/{gc.id}"
                                ultra_headers = BROWSER_HEADERS.copy()
                                ultra_headers["Authorization"] = self.http.token
                                
                                async with self.raw_session.patch(target_url, data=raw_packet, headers=ultra_headers) as resp:
                                    if resp.status == 429:
                                        rate_data = orjson.loads(await resp.read())
                                        retry_after = float(rate_data.get("retry_after", 0.5))
                                        await asyncio.sleep(retry_after)
                                        async with self.raw_session.patch(target_url, data=raw_packet, headers=ultra_headers):
                                            pass
                            except Exception:
                                pass
                                
                        await asyncio.sleep(0.5)
                    except Exception:
                        await asyncio.sleep(1.0)

            # 🚀 200 IQ BROADCAST FIX: 
            # Even if you type this in a GC with only 2 bots, we want ALL active client instances 
            # running on your script to spin up their own loops across their respective GCs.
            # Since all client tasks share the same event loop, we can start the task for this client,
            # and if you want all tokens to execute it universally, you can send the command via your MAIN_OWNER account.
            
            task = asyncio.create_task(math_global_gcnc_loop(), name=f"gcncall_{self.user.id}")
            if message.channel.id not in gcnc_tasks:
                gcnc_tasks[message.channel.id] = []
            gcnc_tasks[message.channel.id].append(task)
            
            await message.channel.send(f"✅ FORB1D🔥 **Hyper-Speed Global GCNC** engaged by **{self.user.name}** across all its GCs: `{base_name}`")

        elif command == "ungcncall":
            killed_count = 0
            
            # Search and cancel all global gcncall tasks across the entire event loop
            for task in asyncio.all_tasks():
                if task.get_name().startswith("gcncall_"):
                    task.cancel()
                    killed_count += 1
            
            await asyncio.sleep(self.user.id % 8 * 0.2)
            if killed_count > 0:
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated global GC name flasher loops across the network.")
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active global GC name flasher running.")

        elif command == "gcjoin":
            # Usage: ^gcjoin <link> OR ^gcjoin @bot <link>
            if len(parts) < 2:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^gcjoin <link>` or `^gcjoin @bot <link>`")
            
            try:
                # Regex pattern matching Discord group chat or invite links
                invite_pattern = r"(?:https?://)?(?:www\.)?(?:discord\.gg|discord\.com/invite|dsc\.gg)/([a-zA-Z0-9-]+)"
                match = re.search(invite_pattern, message.content)
                
                if match:
                    invite_code = match.group(1)
                else:
                    invite_code = parts[-1].split("/")[-1]

                # Target locking check
                if message.mentions:
                    if self.user not in message.mentions:
                        return
                    stagger = random.uniform(0.2, 1.0)
                else:
                    my_math_id = self.user.id % 8 
                    stagger = (my_math_id * 1.5) + random.uniform(0.5, 1.5)
                
                async def join_group_chat():
                    await asyncio.sleep(stagger)
                    try:
                        # Fetch the invite object
                        invite = await self.fetch_invite(invite_code)
                        
                        # Validate if the target invite is actually a Group Chat
                        if invite.guild is not None:
                            await message.channel.send(f"❌ **{self.user.name}** Error: That is a server invite, not a Group Chat link! Use `^serverjoin` instead.")
                            return
                            
                        # Accept the group chat invite
                        await invite.accept()
                        print(f"✅ [{self.user.name}] Successfully joined GC invite {invite_code}", flush=True)
                        await message.channel.send(f"✅ FORB1D🔥 Group Chat infiltrated by **{self.user.name}**.")
                        
                    except discord.NotFound:
                        await message.channel.send(f"❌ **{self.user.name}** Error: Group chat invite is invalid or expired.")
                    except discord.HTTPException as e:
                        # Status 400/403 often indicates the group chat is full or unavailable
                        if e.status == 400 or "maximum number of members" in str(e).lower():
                            await message.channel.send(f"⚠️ **{self.user.name}** Failed: Group chat is completely **filled** or unavailable.")
                        else:
                            await message.channel.send(f"❌ Breach failed for **{self.user.name}**: {e}")
                    except Exception as e:
                        await message.channel.send(f"❌ Error for **{self.user.name}**: {e}")

                asyncio.create_task(join_group_chat())

            except Exception as e:
                if self.user.id % 8 == 0:
                    await message.channel.send(f"❌ Command Error: {e}")
                    

        
        elif command == "sgcnc" or command == "smartgcnc":
            # Usage: ^sgcnc <text> @user1 @user2
            if not message.mentions or len(parts) < 2:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^sgcnc <text> @user1 @user2`")
            
            content_after_cmd = message.content[len(PREFIX) + len(command):].strip()
            custom_text = content_after_cmd
            for mention in message.mentions:
                custom_text = custom_text.replace(f"<@{mention.id}>", "").replace(f"<@!{mention.id}>", "")
            custom_text = custom_text.strip()
            
            if not custom_text:
                return await message.channel.send(f"❌ **{self.user.name}** Error: You must include text for Smart GCNC!")
                
            added_names = []
            for target in message.mentions:
                SGCNC_TARGETS[target.id] = custom_text
                added_names.append(target.name)
            
            current_swarm_size = max(1, len(ACTIVE_SWARM))
            try:
                my_math_id = ACTIVE_SWARM.index(self.user.id)
            except ValueError:
                my_math_id = 0
            await asyncio.sleep((0.2 / current_swarm_size) * my_math_id)
            
            await message.channel.send(f"⚡ FORB1D🔥 **{self.user.name}** armed Smart GCNC text: `{custom_text}` on target(s): `{', '.join(added_names)}`. Waiting for them to change GC name...")

        elif command == "unsgcnc":
            # Usage: ^unsgcnc (clears all) OR ^unsgcnc @user (removes one)
            if message.mentions:
                removed_names = []
                for target in message.mentions:
                    if target.id in SGCNC_TARGETS:
                        del SGCNC_TARGETS[target.id]
                        removed_names.append(target.name)
                
                current_swarm_size = max(1, len(ACTIVE_SWARM))
                try:
                    my_math_id = ACTIVE_SWARM.index(self.user.id)
                except ValueError:
                    my_math_id = 0
                await asyncio.sleep((0.2 / current_swarm_size) * my_math_id)
                
                if removed_names:
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** disarmed Smart GCNC target(s): `{', '.join(removed_names)}`")
                else:
                    await message.channel.send(f"⚠️ None of those users were on the Smart GCNC list.")
            else:
                count = len(SGCNC_TARGETS)
                SGCNC_TARGETS.clear()
                
                current_swarm_size = max(1, len(ACTIVE_SWARM))
                try:
                    my_math_id = ACTIVE_SWARM.index(self.user.id)
                except ValueError:
                    my_math_id = 0
                await asyncio.sleep((0.2 / current_swarm_size) * my_math_id)
                
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** disarmed ALL Smart GCNC targets ({count} users removed).")

        elif command == "sspam" or command == "smartspam":
            # 👑 REMOVED MASTER NODE GUARD SO ANY BOT CAN ARM IT INSTANTLY
            if not message.mentions or len(parts) < 2:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^sspam <text> @user1 @user2 @user3`")
            
            content_after_cmd = message.content[len(PREFIX) + len(command):].strip()
            custom_text = content_after_cmd
            for mention in message.mentions:
                custom_text = custom_text.replace(f"<@{mention.id}>", "").replace(f"<@!{mention.id}>", "")
            custom_text = custom_text.strip()
            
            if not custom_text:
                return await message.channel.send(f"❌ **{self.user.name}** Error: You must include text for Smart Spam!")
                
            added_names = []
            for target in message.mentions:
                SSPAM_TARGETS[target.id] = custom_text
                added_names.append(target.name)
            
            await message.channel.send(f"⚡ FORB1D🔥 Armed Smart Spam text: `{custom_text}` on target(s): `{', '.join(added_names)}`")
            
        elif command == "unsspam":
            # Usage: ^unsspam (clears all) OR ^unsspam @user (removes one)
            if message.mentions:
                removed_names = []
                for target in message.mentions:
                    if target.id in SSPAM_TARGETS:
                        del SSPAM_TARGETS[target.id]
                        removed_names.append(target.name)
                
                current_swarm_size = max(1, len(ACTIVE_SWARM))
                try:
                    my_math_id = ACTIVE_SWARM.index(self.user.id)
                except ValueError:
                    my_math_id = 0
                await asyncio.sleep((0.2 / current_swarm_size) * my_math_id)
                
                if removed_names:
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** disarmed Smart Spam target(s): `{', '.join(removed_names)}`")
                else:
                    await message.channel.send(f"⚠️ None of those users were on the Smart Spam list.")
            else:
                count = len(SSPAM_TARGETS)
                SSPAM_TARGETS.clear()
                
                current_swarm_size = max(1, len(ACTIVE_SWARM))
                try:
                    my_math_id = ACTIVE_SWARM.index(self.user.id)
                except ValueError:
                    my_math_id = 0
                await asyncio.sleep((0.2 / current_swarm_size) * my_math_id)
                
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** disarmed ALL Smart Spam targets ({count} users removed).")

        elif command == "slide":
            # Usage: ^slide @user1 @user2 ...
            if not message.mentions:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^slide @user1 @user2 ...`")
            
            added_names = []
            for target in message.mentions:
                if target.id not in SLIDE_TARGETS:
                    SLIDE_TARGETS.add(target.id)
                    added_names.append(target.name)
            
            await asyncio.sleep(self.user.id % 8 * 0.2)
            if added_names:
                await message.channel.send(f"🎯 FORB1D🔥 **{self.user.name}** locked slide target(s): `{', '.join(added_names)}`")
            else:
                await message.channel.send(f"⚠️ Those users are already on the slide list.")

        elif command == "unslide":
            # Usage: ^unslide (clears all) OR ^unslide @user (removes one)
            if message.mentions:
                removed_names = []
                for target in message.mentions:
                    if target.id in SLIDE_TARGETS:
                        SLIDE_TARGETS.remove(target.id)
                        removed_names.append(target.name)
                
                await asyncio.sleep(self.user.id % 8 * 0.2)
                if removed_names:
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** removed slide target(s): `{', '.join(removed_names)}`")
                else:
                    await message.channel.send(f"⚠️ None of those users were on the slide list.")
            else:
                count = len(SLIDE_TARGETS)
                SLIDE_TARGETS.clear()
                
                await asyncio.sleep(self.user.id % 8 * 0.2)
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** wiped ALL slide targets ({count} users removed).")
                
                
        elif command == "grant":
            # 🛑 LOCK: Only the main owner can authorize new users
            if message.author.id != MAIN_OWNER:
                return await message.channel.send(f"❌ **{self.user.name}** Access Denied: Only the main owner can grant network access.")

            # Usage: ^grant @user
            if not message.mentions:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^grant @user`")
            
            target_user = message.mentions[0]
            
            if target_user.id not in AUTHORIZED_USERS:
                AUTHORIZED_USERS.append(target_user.id)
                await message.channel.send(f"✅ FORB1D🔥 **{target_user.name}** has been granted access to the network by **{self.user.name}**.")
                print(f"🔑 [Security] User {target_user.id} ({target_user.name}) added to AUTHORIZED_USERS.", flush=True)
            else:
                await message.channel.send(f"⚠️ **{target_user.name}** is already authorized on the network.")

        elif command == "ungrant":
            # 🛑 LOCK: Only the main owner can revoke access
            if message.author.id != MAIN_OWNER:
                return await message.channel.send(f"❌ **{self.user.name}** Access Denied: Only the main owner can revoke network access.")

            # Usage: ^ungrant @user
            if not message.mentions:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^ungrant @user`")
            
            target_user = message.mentions[0]
            
            if target_user.id in AUTHORIZED_USERS:
                AUTHORIZED_USERS.remove(target_user.id)
                await message.channel.send(f"🛑 FORB1D🔥 **{target_user.name}** has been revoked of network access by **{self.user.name}**.")
                print(f"🔑 [Security] User {target_user.id} ({target_user.name}) removed from AUTHORIZED_USERS.", flush=True)
            else:
                await message.channel.send(f"⚠️ **{target_user.name}** is not currently authorized on the network.")
                

        elif command == "rs":
            # Usage: !rs <text> <delay>
            if len(parts) < 3:
                return await message.channel.send("❌ Usage: `!rs <text> <delay>`")
            
            try:
                user_text = " ".join(parts[1:-1])
                delay = float(parts[-1])
                
                emojis = ["🔱", "👑", "🔥", "⚡", "💀", "💎", "⚔️"]
                
                # YOUR TEMPLATES LIST: Cycles through these infinitely!
                templates = [
                    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} तेरी माँ की चूत ] ☠️",
    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} तुम मेरा रेप कर रहे हो। ] ☠️",
    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} आपके परिवार के साथ बलात्कार किया गया। ] ☠️",
    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} तेरी माँ को बिना कंडोम के चौदा। ] ☠️",
    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} चल, अपनी औकात बना, गीले टट्टे। ] ☠️",
    "# ╬═❖ 👑 FORBID 👑 ❖═╬ ➔ ☠️ [ {user_text} तेरे बाप को छोड़ दिया। ] ☠️",
    "# █▓▒░ 👑 FORBID KING ║ ➔ 🪓 **{user_text} SON OF FAGG0T** ⪧ 【💀】",
    "# █▓▒░ 👑 FORBID KING ║ ➔ ⚡ **{user_text} FXKEED UR MOM RAW** ⪧ 【🔥】",
    "# █▓▒░ 👑 FORBID KING ║ ➔ 🌌 **{user_text} घी खत्म हो गया है।** ⪧ 【🤯】",
    "# █▓▒░ 👑 FORBID KING ║ ➔ 🛑 **{user_text} BITCH** ⪧ 【😂】",
    "# █▓▒░ 👑 FORBID KING ║ ➔ ⚔️ **{user_text} CUDKAD** ⪧ 【💥】",
    "# █▓▒░ 👑 FORBID KING ║ ➔ 👿 **{user_text} GULAMI KR** ⪧ 【🔱】"
                ]

                async def spam_loop():
                    # ⚡ CHANGED: client.user.id -> self.user.id
                    # 🟢 ENTERPRISE MATH: Auto-adjusts to the live swarm size!
                    current_swarm_size = max(1, len(ACTIVE_SWARM))
                    
                    try:
                        # Bot finds its exact place in the live line-up (0, 1, 2, 3...)
                        my_math_id = ACTIVE_SWARM.index(self.user.id)
                    except ValueError:
                        my_math_id = 0
                        
                    perfect_stagger = (delay / float(current_swarm_size)) * my_math_id
                    
                    # ⚡ CHANGED: client.user.id -> self.user.id
                    emoji_index = self.user.id % len(emojis)
                    template_index = self.user.id % len(templates)
                    
                    await asyncio.sleep(perfect_stagger)

                    while True:
                        try:
                            chosen_emoji = emojis[emoji_index]
                            emoji_index = (emoji_index + 1) % len(emojis)
                            
                            raw_template = templates[template_index]
                            template_index = (template_index + 1) % len(templates)
                            
                            base_text = raw_template.replace("{user_text}", user_text).replace("{chosen_emoji}", chosen_emoji)
                            spaced_text = base_text.replace(" ", " \u200B")
                            
                            line_length = len(spaced_text) + 2
                            multiplier = 1950 // line_length
                            if multiplier < 1: multiplier = 1
                            
                            final_content = "\n\n".join([spaced_text] * multiplier)
                            
                            # 🚀 PURE SOCKET INJECTION INSTEAD
                            url = f"https://discord.com/api/v9/channels/{message.channel.id}/messages"
                            payload = {"content": final_content}
                            
                            async with self.raw_session.post(url, json=payload) as response:
                                if response.status == 429:
                                    rate_data = await response.json()
                                    retry_after = rate_data.get("retry_after", 1.0)
                                    
                                    # 🟢 THIS IS THE NEW PART YOU NEED TO ADD:
                                    global global_last_log
                                    if time.time() - global_last_log > 60:
                                        print(f"⚠️ [System] Network Rate Limit hit. Pausing for {retry_after}s. (Muting further logs for 60s)", flush=True)
                                        global_last_log = time.time()
                                        
                                    await asyncio.sleep(retry_after)
                                else:
                                    await asyncio.sleep(delay)
                        
                        except Exception as e:
                            print(f"⚠️ Socket Error: {e}", flush=True)
                            await asyncio.sleep(0.1)
                
                task = asyncio.create_task(spam_loop(), name=f"spam_{message.channel.id}")
                
                # ⚡ ADDED: Explicit global call so it finds your dictionary
                
                if message.channel.id not in spam_tasks:
                    spam_tasks[message.channel.id] = []
                spam_tasks[message.channel.id].append(task)
                
                # ⚡ CHANGED: client.user.id -> self.user.id
                if self.user.id % 8 == 0 or self.user.id % 8 == 1: 
                    await message.channel.send(f"✅ FORB1D🔥 Template-Cycling Math Spam started.")
            
            except Exception as e:
                await message.channel.send(f"❌ Error: {e}")


        elif command == "cs":
            # Usage: !cs <text> <delay>
            if len(parts) < 3:
                return await message.channel.send("❌ Usage: `!cs <text> <delay>`")
            
            try:
                # 🏎️ RUST & MEMORY MODULES LOADED JUST FOR THIS COMMAND
                import orjson
                import gc
                
                user_text = " ".join(parts[1:-1])
                delay = float(parts[-1])
                hearts = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎"]

                # -----------------------------------------------------------------
                # 🔥 THE FORGE: PRE-BAKE ALL PAYLOADS TO RAW RUST BYTES
                # -----------------------------------------------------------------
                pre_baked_bytes = []
                for heart in hearts:
                    base_text = f"# {user_text} - ({heart})"
                    spaced_text = base_text.replace(" ", " \u200B")
                    multiplier = 1950 // (len(spaced_text) + 2)
                    final_content = "\n\n".join([spaced_text] * max(1, multiplier))
                    
                    # Convert to raw JSON byte format instantly using Rust
                    raw_json_bytes = orjson.dumps({"content": final_content})
                    pre_baked_bytes.append(raw_json_bytes)

                async def custom_loop():
                    global global_last_log
                    
                    local_sleep = asyncio.sleep
                    local_time = time.time
                    local_post = self.raw_session.post  # Direct reference
                    local_bytes = pre_baked_bytes
                    local_len = len(hearts)
                    
                    current_swarm_size = max(1, len(ACTIVE_SWARM))
                    
                    try:
                        my_math_id = ACTIVE_SWARM.index(self.user.id)
                    except ValueError:
                        my_math_id = 0
                        
                    perfect_stagger = (delay / float(current_swarm_size)) * my_math_id
                    color_index = self.user.id % local_len
                    
                    await local_sleep(perfect_stagger)
                    
                    # 🔥 SPEED HACK 1: Static string allocation OUTSIDE the loop
                    target_url = f"https://discord.com/api/v9/channels/{message.channel.id}/messages"
                    
                    # Merge token with global browser headers
                    ultra_headers = BROWSER_HEADERS.copy()
                    ultra_headers["Authorization"] = self.http.token
                    
                    gc.disable() 
                    
                    try:
                        while True:
                            try:
                                raw_packet = local_bytes[color_index]
                                color_index = (color_index + 1) % local_len
                                
                                # 🔥 SPEED HACK 2: Fire direct request without creating an async context frame
                                response = await local_post(target_url, data=raw_packet, headers=ultra_headers)
                                
                                if response.status == 429:
                                    gc.enable() 
                                    rate_data = orjson.loads(await response.read())
                                    retry_after = rate_data.get("retry_after", 0.5)
                                    
                                    if local_time() - global_last_log > 60:
                                        print(f"⚠️ Rate Limit: Pausing Node for {retry_after}s.", flush=True)
                                        global_last_log = local_time()
                                        
                                    await local_sleep(retry_after)
                                    gc.disable() 
                                else:
                                    # If delay is 0, this yields control back to uvloop instantly
                                    if delay > 0:
                                        await local_sleep(delay)
                                    else:
                                        await asyncio.sleep(0) # Keep event loop alive without blocking
                                        
                            except Exception as e:
                                gc.enable()
                                print(f"⚠️ Socket Exception: {e}", flush=True)
                                await local_sleep(0.001)
                                gc.disable()
                    finally:
                        gc.enable() 
                    
                    try:
                        while True:
                            try:
                                # Pure array indexing—takes less than a microsecond
                                raw_packet = local_bytes[color_index]
                                color_index = (color_index + 1) % local_len
                                
                                # Send raw bytes, completely bypassing Python's slow JSON layer
                                async with local_post(url, data=raw_packet, headers=ultra_headers) as response:
                                    if response.status == 429:
                                        gc.enable() # Unfreeze to process limits
                                        
                                        # Use Rust to read the rate limit data instantly
                                        rate_data = orjson.loads(await response.read())
                                        retry_after = rate_data.get("retry_after", 1.0)
                                        
                                        if local_time() - global_last_log > 60:
                                            print(f"⚠️ [System] Network Rate Limit hit. Pausing for {retry_after}s. (Muting further logs for 60s)", flush=True)
                                            global_last_log = local_time()
                                            
                                        await local_sleep(retry_after)
                                        gc.disable() # Re-freeze runtime
                                    else:
                                        # Zero execution time loop pacing
                                        await local_sleep(delay)
                                        
                            except Exception as e:
                                gc.enable()
                                print(f"⚠️ High-Speed Socket Exception: {e}", flush=True)
                                await local_sleep(0.01)
                                gc.disable()
                    finally:
                        # ALWAYS ensure memory unfreezes if the loop somehow breaks
                        gc.enable()
                
                # Deploy execution task straight into the C-accelerated engine
                task = asyncio.create_task(custom_loop(), name=f"spam_{message.channel.id}")
                
                if message.channel.id not in spam_tasks:
                    spam_tasks[message.channel.id] = []
                spam_tasks[message.channel.id].append(task)
                
                # Prevent 8 identical confirmations
                if self.user.id % 8 == 0 or self.user.id % 8 == 1: 
                    await message.channel.send(f"🌌 **UNIVERSAL SPEEDS ATTAINED.** Hyper-Engine Online: '{user_text}'")
            
            except Exception as e:
                await message.channel.send(f"❌ Critical Core Error: {e}")

        elif command == "fs" or command == "forwardspam":
            if len(parts) < 3:
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `^fs <text> <delay>`")
            
            try:
                import orjson
                import gc
                
                user_text = " ".join(parts[1:-1])
                delay = float(parts[-1])
                
                # 🔥 LETHAL HATER EMOJI POOL
                emojis = ["💀", "👑", "⚡", "🔥", "🔪", "🗡️", "⚔️", "🩸", "☠️", "🔱"]
                
                # 🔥 ELITE FORB1D SOVEREIGN SYSTEM CARD TEMPLATES
                forward_styles = [
                    "👑 **【 F O R B 1 D   K I N G   M A J E S T Y 】** 👑\n> ⚡ *HEIR TO THE THRONE OF ABSOLUTE TERROR*\n> ☠️ `{user_text} ({chosen_emoji})`",
                    "⚔️ **【 F O R B 1 D   K I N G   R U L E 】** ⚔️\n> 🩸 *BOW DOWN TO THE KING OF KINGS*\n> 👑 `{user_text} ({chosen_emoji})`",
                    "🔥 **【 F O R B 1 D   K I N G   D E C R E E 】** 🔥\n> 🔱 *THE SUPREME RULER HAS SPOKEN*\n> 💀 `{user_text} ({chosen_emoji})`"
                ]

                # -----------------------------------------------------------------
                # 🔥 THE FORGE: PRE-BAKE STACKED FORB1D CARDS TO RAW RUST BYTES
                # -----------------------------------------------------------------
                pre_baked_forward_bytes = []
                for style in forward_styles:
                    for emoji in emojis:
                        base_text = style.replace("{user_text}", user_text).replace("{chosen_emoji}", emoji)
                        spaced_text = base_text.replace(" ", " \u200B")
                        
                        # Scale it up big to fill the message block instantly
                        multiplier = 1950 // (len(spaced_text) + 2)
                        if multiplier < 1: multiplier = 1
                        
                        final_content = "\n\n".join([spaced_text] * multiplier)
                        raw_json_bytes = orjson.dumps({"content": final_content})
                        pre_baked_forward_bytes.append(raw_json_bytes)

                async def forward_loop():
                    global global_last_log
                    local_sleep = asyncio.sleep
                    local_time = time.time
                    local_post = self.raw_session.post
                    local_bytes = pre_baked_forward_bytes
                    local_len = len(local_bytes)
                    
                    current_swarm_size = max(1, len(ACTIVE_SWARM))
                    try:
                        my_math_id = ACTIVE_SWARM.index(self.user.id)
                    except ValueError:
                        my_math_id = 0
                        
                    perfect_stagger = (delay / float(current_swarm_size)) * my_math_id
                    packet_index = (self.user.id + int(time.time())) % local_len
                    
                    await local_sleep(perfect_stagger)
                    
                    target_url = f"https://discord.com/api/v9/channels/{message.channel.id}/messages"
                    
                    # Merge token with global browser headers
                    ultra_headers = BROWSER_HEADERS.copy()
                    ultra_headers["Authorization"] = self.http.token
                    
                    gc.disable()
                    try:
                        while True:
                            try:
                                raw_packet = local_bytes[packet_index]
                                packet_index = (packet_index + 1) % local_len
                                
                                response = await local_post(target_url, data=raw_packet, headers=ultra_headers)
                                
                                if response.status == 429:
                                    gc.enable()
                                    rate_data = orjson.loads(await response.read())
                                    retry_after = rate_data.get("retry_after", 0.5)
                                    
                                    if local_time() - global_last_log > 60:
                                        print(f"⚠️ [System] Forward Rate Limit hit. Pausing Node for {retry_after}s.", flush=True)
                                        global_last_log = local_time()
                                        
                                    await local_sleep(retry_after)
                                    gc.disable()
                                else:
                                    if delay > 0:
                                        await local_sleep(delay)
                                    else:
                                        await asyncio.sleep(0)
                                        
                            except Exception as e:
                                gc.enable()
                                print(f"⚠️ Forward Socket Exception: {e}", flush=True)
                                await local_sleep(0.01)
                                gc.disable()
                    finally:
                        gc.enable()

                task = asyncio.create_task(forward_loop(), name=f"forward_{message.channel.id}")
                
                if message.channel.id not in spam_tasks:
                    spam_tasks[message.channel.id] = []
                spam_tasks[message.channel.id].append(task)
                
                if self.user.id % 8 == 0 or self.user.id % 8 == 1: 
                    await message.channel.send(f"📦 **FORB1D SOVEREIGN FORWARD ENGINE ONLINE.**")
            
            except Exception as e:
                await message.channel.send(f"❌ Core Error: {e}")

        elif command == "unfs" or command == "unforwardspam":
            killed = False
            for task in asyncio.all_tasks():
                if task.get_name() == f"forward_{message.channel.id}":
                    task.cancel()
                    killed = True
            
            await asyncio.sleep(self.user.id % 8 * 1.0)
            if killed:
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated all forward spam loops here.")
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active forward spam in this channel.")



        # =========================================================
        # 🛑 YOU WERE MISSING THIS HEADER RIGHT HERE 🛑
        # =========================================================
        elif command == "unspam":
            
            # Direct Core Search: Find and kill tasks by their hidden registry names
            killed = False
            for task in asyncio.all_tasks():
                if task.get_name() == f"spam_{message.channel.id}":
                    task.cancel()
                    killed = True
            
            # Staggered confirmation so all 8 bots reply cleanly
            await asyncio.sleep(self.user.id % 8 * 1.0)
            if killed:
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated all zombie spam loops here.")
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active spam in this channel.")

        elif command == "serverjoin":
            # Usage: !serverjoin <link> OR !serverjoin @bot <link>
            if len(parts) < 2:
                return await message.channel.send("❌ Usage: `!serverjoin <link>` or `!serverjoin @bot <link>`")
            
            try:
                # 1. Regex to pull the exact code from ANYWHERE in the message
                invite_pattern = r"(?:https?://)?(?:www\.)?(?:discord\.gg|discord\.com/invite|dsc\.gg)/([a-zA-Z0-9-]+)"
                match = re.search(invite_pattern, message.content)
                
                if match:
                    invite_code = match.group(1)
                else:
                    invite_code = parts[-1].split("/")[-1]

                # 2. TARGET LOCKING
                if message.mentions:
                    # If this specific token is NOT in the mentions, ignore completely
                    if self.user not in message.mentions:
                        return
                    
                    stagger = random.uniform(0.2, 1.0)
                else:
                    # No mentions = ALL tokens join. Use the math Gatling stagger
                    my_math_id = self.user.id % 8 
                    stagger = (my_math_id * 1.5) + random.uniform(0.5, 1.5)
                
                print(f"[{self.user.name}] Engaging infiltration protocol. Stagger: {stagger:.2f}s...", flush=True)
                
                async def join_server():
                    await asyncio.sleep(stagger)
                    try:
                        invite = await self.fetch_invite(invite_code)
                        await invite.accept()
                        print(f"✅ [{self.user.name}] Successfully joined {invite_code}", flush=True)
                        
                        # ⚡ CHANGED: Every bot that joins will now announce it in chat
                        await message.channel.send(f"✅ FORB1D🔥 Network infiltrated by **{self.user.name}**: `{invite_code}`")
                            
                    except Exception as e:
                        print(f"❌ [{self.user.name}] Join failed: {e}", flush=True)
                        # Every bot that fails will also report its failure
                        await message.channel.send(f"❌ Breach failed for **{self.user.name}**: {e}")

                # Run in background
                asyncio.create_task(join_server())

            except Exception as e:
                if self.user.id % 8 == 0:
                    await message.channel.send(f"❌ Command Error: {e}")

        elif command == "serverleave":
            # Usage: !serverleave <link> OR !serverleave @bot <link>
            if len(parts) < 2:
                return await message.channel.send("❌ Usage: `!serverleave <link>` or `!serverleave @bot <link>`")
            
            try:
                # 1. Regex to pull the exact code from ANYWHERE in the message
                invite_pattern = r"(?:https?://)?(?:www\.)?(?:discord\.gg|discord\.com/invite|dsc\.gg)/([a-zA-Z0-9-]+)"
                match = re.search(invite_pattern, message.content)
                
                if match:
                    invite_code = match.group(1)
                else:
                    invite_code = parts[-1].split("/")[-1]

                # 2. TARGET LOCKING: Check if specific bots were mentioned
                if message.mentions:
                    if self.user not in message.mentions:
                        return
                    # Fast extraction for targeted bots
                    stagger = random.uniform(0.2, 1.0)
                    is_targeted = True
                else:
                    # Math stagger for full wave extraction to avoid API spam flags
                    my_math_id = self.user.id % 8 
                    stagger = (my_math_id * 1.0) + random.uniform(0.2, 1.0)
                    is_targeted = False
                
                print(f"[{self.user.name}] Engaging extraction protocol. Stagger: {stagger:.2f}s...", flush=True)
                
                async def leave_server():
                    await asyncio.sleep(stagger)
                    try:
                        # Fetch the invite to identify WHICH server it belongs to
                        invite = await self.fetch_invite(invite_code)
                        guild_id = invite.guild.id
                        
                        # Check if the bot is actually inside this specific server
                        guild_to_leave = self.get_guild(guild_id)
                        
                        if guild_to_leave:
                            await guild_to_leave.leave()
                            print(f"✅ [{self.user.name}] Successfully extracted from {guild_to_leave.name}", flush=True)
                            
                            # ⚡ CHANGED: Every bot that successfully leaves will now announce it
                            await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** extracted from: `{guild_to_leave.name}`")
                        else:
                            print(f"⚠️ [{self.user.name}] Aborted: Not in network {invite_code}", flush=True)
                            
                            # ⚡ CHANGED: Every bot will announce if it wasn't in the server
                            await message.channel.send(f"⚠️ **{self.user.name}** is not in that network.")
                                
                    except Exception as e:
                        print(f"❌ [{self.user.name}] Extraction failed: {e}", flush=True)
                        
                        # ⚡ CHANGED: Every bot that hits an error will report it
                        await message.channel.send(f"❌ Extraction failed for **{self.user.name}**: {e}")

                # Run in background
                asyncio.create_task(leave_server())

            except Exception as e:
                # We leave this outer one filtered so if the link itself is completely broken, 
                # you only get 1 error message instead of 8 identical ones.
                if self.user.id % 8 == 0:
                    await message.channel.send(f"❌ Command Error: {e}")

        elif command == "autoreact":
            # Usage: !autoreact @user 💀
            if not message.mentions or len(parts) < 3:
                return await message.channel.send("❌ Usage: `!autoreact @user <emoji>`")
            
            target_id = message.mentions[0].id
            chosen_emoji = parts[-1]
            
            # Lock the target and emoji into the global brain
            AUTO_REACT_TARGETS[target_id] = chosen_emoji
            
            # ⚡ ALL bots respond confirming the lock-on!
            await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** Locked on! Auto-reacting {chosen_emoji} to <@{target_id}>")

        elif command == "unautoreact":
            # Usage: !unautoreact (clears all) OR !unautoreact @user (clears one)
            if message.mentions:
                # 1. PRECISION STRIKE CANCEL: Only stop for the mentioned user
                target_id = message.mentions[0].id
                
                if target_id in AUTO_REACT_TARGETS:
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** disengaged from <@{target_id}>")
                    await asyncio.sleep(0.5)
                    
                    if target_id in AUTO_REACT_TARGETS:
                        del AUTO_REACT_TARGETS[target_id]
                else:
                    await message.channel.send(f"⚠️ **{self.user.name}** was not targeting that user.")
                    
            else:
                # 2. TOTAL SYSTEM WIPE: No mentions, so clear EVERY target
                if AUTO_REACT_TARGETS:
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** wiped ALL auto-react targets!")
                    await asyncio.sleep(0.5)
                    
                    AUTO_REACT_TARGETS.clear()
                else:
                    await message.channel.send(f"⚠️ **{self.user.name}** has no active targets to clear.")

        elif command == "gcnc":
            # Usage: !gcnc <name> <delay>
            if len(parts) < 3:
                await asyncio.sleep(random.uniform(0.1, 0.5))
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `!gcnc <name> <delay>` (e.g. !gcnc testing 1)")

            # 1. Security Check: Only run this if we are actually in a Group Chat
            if not isinstance(message.channel, discord.GroupChannel):
                await asyncio.sleep(random.uniform(0.1, 0.5))
                return await message.channel.send(f"❌ FORB1D🔥 Error: **{self.user.name}** - This command only works in Group Chats.")

            try:
                # Everything in the middle is the name, the very last part is the delay
                base_name = " ".join(parts[1:-1])
                delay = float(parts[-1])
                emojis = ["💀", "👿", "🔥", "👑", "⚡", "🔱", "💎", "☠️"]
                
                # YOUR GC NAME TEMPLATES: Cycles through these infinitely!
                # YOUR GC NAME TEMPLATES: Designed to be massive and hit the 100-character hard limit!
                templates = [
    "{chosen_emoji} 𝗙𝗢𝗥𝗕𝟭𝗗 𝗞𝗜𝗡𝗚 【 {user_text} 】 ﷽﷽﷽﷽﷽﷽",
    "{chosen_emoji} ＦＯＲＢ１Ｄ ＫＩＮＧ ꧅ {user_text} ꧅ 𒐫𒐫𒐫𒐫𒐫𒐫",
    "{chosen_emoji} 𝐅𝐎𝐑𝐁𝟏𝐃 𝐊𝐈𝐍𝐆 ☠️ {user_text} ☠️ 𒈙𒈙𒈙𒈙𒈙𒈙",
    "{chosen_emoji} 𝙁𝙊𝙍𝘽1𝘿 𝙆𝙄𝙉𝙂 ⚡ {user_text} ⚡ ꧅꧅꧅꧅꧅꧅",
    "{chosen_emoji} 𝗙𝗢𝗥𝗕𝟭𝗗 𝗞𝗜𝗡𝗚 ╳ {user_text} ╳ ﷽𒐫﷽𒐫﷽𒐫",
    "{chosen_emoji} ＦＯＲＢ１Ｄ ＫＩＮＧ 👑 {user_text} 👑 𒈙꧅𒈙꧅𒈙꧅",
    "{chosen_emoji} 𝐅𝐎𝐑𝐁𝟏𝐃 𝐊𝐈𝐍𝐆 ░ {user_text} ░ ﷽𒈙﷽𒈙﷽𒈙",
    "{chosen_emoji} 𝙁𝙊𝙍𝘽1𝘿 𝙆𝙄𝙉𝙂 💥 {user_text} 💥 𒐫꧅𒐫꧅𒐫꧅",
    "{chosen_emoji} 𝗙𝗢𝗥𝗕𝟭𝗗 𝗞𝗜𝗡𝗚 𒈙 {user_text} 𒈙 ﷽﷽﷽﷽﷽﷽",
    "{chosen_emoji} ＦＯＲＢ１Ｄ ＫＩＮＧ ★ {user_text} ★ ꧅𒐫𒈙꧅𒐫𒈙"
]
                
                # 🟢 ENTERPRISE MATH: Gatling Gun Synchronization & Limit Surfing
                async def gcnc_loop():
                    current_swarm_size = max(1, len(ACTIVE_SWARM))
                    
                    try:
                        # Bot finds its exact place in the live line-up
                        my_math_id = ACTIVE_SWARM.index(self.user.id)
                    except ValueError:
                        my_math_id = 0
                        
                    # 🔥 THE GATLING GUN MATH 🔥
                    # Perfectly spaces the bots out. If delay is 1s and 5 bots are running:
                    # Bot 0 waits 0.0s | Bot 1 waits 0.2s | Bot 2 waits 0.4s...
                    # Result: The GC name changes perfectly every 0.2 seconds!
                    micro_stagger = my_math_id * (delay / current_swarm_size)
                    await asyncio.sleep(micro_stagger)
                    
                    # Offset the starting emojis/templates so they don't look identical
                    emoji_index = my_math_id % len(emojis)
                    template_index = my_math_id % len(templates)
                    
                    while True:
                        try:
                            # Cycle Emoji
                            chosen_emoji = emojis[emoji_index]
                            emoji_index = (emoji_index + 1) % len(emojis)
                            
                            # Cycle Template
                            raw_template = templates[template_index]
                            template_index = (template_index + 1) % len(templates)
                            
                            # Swap placeholders
                            new_gc_name = raw_template.replace("{user_text}", base_name).replace("{chosen_emoji}", chosen_emoji)
                            
                            # Max limit safety check (GC names cap at 100 chars)
                            if len(new_gc_name) > 100:
                                new_gc_name = new_gc_name[:100]
                            
                            # 🚀 FIRE THE EDIT IMMEDIATELY
                            await message.channel.edit(name=new_gc_name)
                            
                            # ⚡ NO CYCLE WAITING. Just wait your personal base delay. 
                            # The micro_stagger handles the overlap natively!
                            await asyncio.sleep(delay) 
                            
                        except discord.HTTPException as e:
                            if e.status == 429:
                                # 🎯 SNIPER RECOVERY: Read exact penalty, wait it + 0.05s buffer, fire instantly
                                wait = float(e.response.headers.get("Retry-After", 1.0))
                                await asyncio.sleep(wait + 0.05)
                            else:
                                # Generic network glitch, wait half a second and push through
                                await asyncio.sleep(0.5)

                # Fire it in the background
                task = asyncio.create_task(gcnc_loop(), name=f"gcnc_{message.channel.id}")
                
                # SEPARATED SYSTEM: We use a brand new dictionary so !unspam ignores it
                if message.channel.id not in gcnc_tasks:
                    gcnc_tasks[message.channel.id] = []
                gcnc_tasks[message.channel.id].append(task)
                
                # ⚡ JITTER REMOVED FOR MAXIMUM SPEED. Instant confirmation.
                await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** OVERRIDE ENGAGED. Delay: `{delay}s` | Targets: `{base_name}`")
            
            except ValueError:
                await message.channel.send(f"❌ **{self.user.name}** Error: Delay must be a number (e.g. 1.5).")
            except Exception as e:
                await message.channel.send(f"❌ **{self.user.name}** Command Error: {e}")

        # =========================================================
        # 🛑 ADD THIS HEADER SO IT DOESN'T AUTO-KILL ITSELF 🛑
        # =========================================================
        elif command == "ungcnc":

            # Direct Core Search for GC tasks
            killed = False
            for task in asyncio.all_tasks():
                if task.get_name() == f"gcnc_{message.channel.id}":
                    task.cancel()
                    killed = True
            
            # Jittered confirmation
            jitter = random.uniform(0.1, 0.6)
            await asyncio.sleep(jitter)
            
            if killed:
                await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** terminated GC Name Flasher here.")
                print(f"🛑 [{self.user.name}] Stopped gcnc tasks in GC: {message.channel.id}", flush=True)
            else:
                await message.channel.send(f"⚠️ **{self.user.name}** found no active FORB1D🔥 GC Name Flasher running here.")


        elif command == "gcleave":
            # Usage: !gcleave (this GC) | !gcleave @bot (target bot) | !gcleave all (every GC)
            mode = "current"
            if len(parts) > 1:
                if parts[1].lower() == "all":
                    mode = "all"
                elif message.mentions:
                    mode = "targeted"
            
            # Base jitter so the 8 bots don't hit Discord's message endpoint at the exact same ms
            jitter = random.uniform(0.1, 0.6)

            if mode == "targeted":
                # If this specific bot was NOT mentioned, it ignores the command completely
                if self.user not in message.mentions:
                    return
                
                if message.channel.type != discord.ChannelType.group:
                    await asyncio.sleep(jitter)
                    return await message.channel.send(f"❌ **{self.user.name}** Error: This is not a Group Chat.")
                
                # It MUST send the message BEFORE leaving, otherwise Discord blocks the message!
                await asyncio.sleep(jitter)
                await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** is extracting from this GC.")
                
                await asyncio.sleep(0.5) # Wait half a second to ensure the message sent
                await message.channel.leave()
                print(f"✅ [{self.user.name}] Left GC: {message.channel.id}", flush=True)

            elif mode == "current":
                # Standard !gcleave (all bots leave this specific GC)
                if message.channel.type != discord.ChannelType.group:
                    await asyncio.sleep(jitter)
                    return await message.channel.send(f"❌ **{self.user.name}** Error: This is not a Group Chat.")
                
                await asyncio.sleep(jitter)
                await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** is extracting from this GC.")
                
                await asyncio.sleep(0.5)
                await message.channel.leave()
                print(f"✅ [{self.user.name}] Left GC: {message.channel.id}", flush=True)

            elif mode == "all":
                # Get a list of every single GC the bot is currently inside
                gcs_to_leave = [ch for ch in self.private_channels if isinstance(ch, discord.GroupChannel)]
                
                # 200 IQ PLAY: If we are currently standing in a GC, we must leave it LAST.
                # Otherwise, the bot will lose access to the channel and can't send the final message!
                current_is_gc = isinstance(message.channel, discord.GroupChannel)
                if current_is_gc and message.channel in gcs_to_leave:
                    gcs_to_leave.remove(message.channel)
                
                leave_count = 0
                for gc in gcs_to_leave:
                    try:
                        await gc.leave()
                        leave_count += 1
                        # Stealth delay between leaves so Discord doesn't flag the account
                        await asyncio.sleep(random.uniform(0.8, 2.0))
                    except Exception as e:
                        print(f"❌ [{self.user.name}] Failed to leave GC {gc.id}: {e}", flush=True)
                
                # Now that the background wipe is done, ALL bots report their total count
                await asyncio.sleep(jitter)
                total_left = leave_count + (1 if current_is_gc else 0)
                # Creates a perfect 1-second line-up based on the bot's ID
                await asyncio.sleep(self.user.id % 8 * 1.0)
                await message.channel.send(f"✅ FORB1D🔥 **{self.user.name}** successfully extracted from {total_left} GCs.")
                print(f"✅ [{self.user.name}] Mass GC extraction complete.", flush=True)
                
                # FINALLY: Leave the current GC as the absolute last step
                if current_is_gc:
                    await asyncio.sleep(0.5)
                    await asyncio.sleep(1.0)
                    await message.channel.leave()

        elif command == "stream":
            # Usage: !stream <Text> (Turns it on) | !stream stop (Turns it off)
            if len(parts) < 2:
                await asyncio.sleep(self.user.id % 8 * 1.0)
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `!stream <text>` or `!stream stop`")

            stream_text = " ".join(parts[1:])
            
            # STAGGER MATH: So all 8 bots don't hit the Discord presence API at the exact same millisecond
            stagger = (self.user.id % 8 * 1.0) + random.uniform(0.1, 0.5)
            await asyncio.sleep(stagger)

            try:
                if stream_text.lower() == "stop":
                    # Clear the rich presence (turns off the streaming status)
                    await self.change_presence(activity=None)
                    
                    await asyncio.sleep(0.5)
                    await message.channel.send(f"🛑 FORB1D🔥 **{self.user.name}** stopped streaming.")
                else:
                    # Discord requires a Twitch or YT link for the purple stream icon to appear
                    twitch_url = "https://www.twitch.tv/forb1d"
                    
                    # Lock in the Streaming status
                    activity = discord.Streaming(name=stream_text, url=twitch_url)
                    await self.change_presence(activity=activity)
                    
                    await asyncio.sleep(0.5)
                    await message.channel.send(f"🟣 FORB1D🔥 **{self.user.name}** is now streaming: `{stream_text}`")
                    
            except Exception as e:
                await message.channel.send(f"❌ **{self.user.name}** Failed to update status: {e}")

        elif command == "presence":
            # Usage: !presence <play/listen/watch> <text>
            if len(parts) < 3:
                await asyncio.sleep(self.user.id % 8 * 1.0)
                return await message.channel.send(f"❌ **{self.user.name}** Usage: `!presence <play/listen/watch> <text>`")

            activity_type = parts[1].lower()
            presence_text = " ".join(parts[2:])

            # STAGGER MATH: Perfect 1-second intervals so the API doesn't flag the sudden mass-update
            stagger = (self.user.id % 8 * 1.0) + random.uniform(0.1, 0.5)
            await asyncio.sleep(stagger)

            try:
                if activity_type == "play":
                    act = discord.Game(name=presence_text)
                    msg = f"🎮 FORB1D🔥 **{self.user.name}** is playing: `{presence_text}`"
                elif activity_type == "listen":
                    act = discord.Activity(type=discord.ActivityType.listening, name=presence_text)
                    msg = f"🎧 FORB1D🔥 **{self.user.name}** is listening to: `{presence_text}`"
                elif activity_type == "watch":
                    act = discord.Activity(type=discord.ActivityType.watching, name=presence_text)
                    msg = f"📺 FORB1D🔥 **{self.user.name}** is watching: `{presence_text}`"
                else:
                    return await message.channel.send(f"❌ **{self.user.name}** Invalid mode! Use play, listen, or watch.")

                # Lock in the new status
                await self.change_presence(activity=act)
                
                await asyncio.sleep(0.5)
                await message.channel.send(msg)

            except Exception as e:
                await message.channel.send(f"❌ **{self.user.name}** Failed to update presence: {e}")

        elif command == "help":
            # STAGGER MATH: All 8 bots respond, staggered by 1 second so Discord doesn't block them!
            stagger = (self.user.id % 8 * 1.0) + random.uniform(0.1, 0.4)
            await asyncio.sleep(stagger)
            
            # Wrapped in ```yaml to give it that colored, luxury terminal aesthetic in Discord
            help_panel = f"""```yaml
🔥 FORB1D OPS | MASTER CONTROL 🔥
=====================================
"Dominate the network. Engineered by FORB1D🔥"

[ 📡 INFILTRATION & EXTRACTION ]
> ^serverjoin <link>    (Swarm joins)
> ^serverjoin @bot      (Precision join)
> ^serverleave <link>   (Swarm leaves)
> ^serverleave @bot     (Precision leave)
> ^ping                 (Live latency)
> ^unping               (Stop live latency)
> ^reset                (Refresh Whole Script)

[ 👥 GROUP CHAT OPS ]
> ^gcjoin <link>        (Join GC Through Link)
> ^gcnc <name> <delay>  (GC Name Flasher)
> ^ungcnc               (Stop flasher here)
> ^gcleave              (Swarm leaves this GC)
> ^gcleave all          (Swarm leaves ALL GCs)
> ^gcleave @bot         (Precision GC leave)
> ^sgcnc <text> @userx  (Fastest-GCNC!)
> ^unsgcnc @user        (Disarms Smart GCNC targets)
> ^gcspamall <text>     (Spam In Every Gc OP)
> ^gcncall <text>       (GCNC In Every Gc OP)
> ^ungcspamall          (Stop All Spam In Gc's)
> ^ungcncall            (Stop All GCNC)
> ^gccall               (Spam Call In GC)
> ^ungccall             (Stop Spam Calls)

[ 🎯 TARGETING & SPAM OPS ]
> ^autoreact @user 💀   (Lock-on reactions)
> ^unautoreact          (Wipe all targets)
> ^unautoreact @user    (Unlock specific user)
> ^rs <text> <delay>    (Roast Chat Spam)
> ^cs <text> <delay>    (Custom Spam)
> ^fs <text> <delay>    (Forwarded Spam)
> ^sspam <text> @user1  (Fastest Smart Spam)
> ^unsspam @user        (Stop Smart Spam)
> ^unspam               (Stop Chat Spam)
> ^slide @user1 @user2  (Auto Roaster)
> ^unslide @user @user2 (Precise Remover)

[ 🎭 FLEX & PRESENCE OPS ]
> ^grant @user          (Grant Access)
> ^ungrant @user        (Revoke Access)
> ^stream <text>        (Purple stream status)
> ^stream stop          (Wipe stream status)
> ^presence <mode> <msg>(play/listen/watch)

=====================================
⚡ Powered by FORB1D🔥 Network ⚡
[ {self.user.name} - System Online ]
```"""
            try:
                await message.channel.send(help_panel)
            except Exception as e:
                print(f"❌ [{self.user.name}] Help Panel failed: {e}", flush=True)

       
    async def ram_cleaner_loop(self):
        import gc
        await self.wait_until_ready()
        if self.user.id % 8 != 0:
            return
        while not self.is_closed():
            try:
                await asyncio.sleep(600)
                collected = gc.collect()
                for channel_id in list(spam_tasks.keys()):
                    if channel_id in spam_tasks and not spam_tasks[channel_id]:
                        del spam_tasks[channel_id]
                for channel_id in list(gcnc_tasks.keys()):
                    if channel_id in gcnc_tasks and not gcnc_tasks[channel_id]:
                        del gcnc_tasks[channel_id]
                print(f"🧹 [Memory Engine] Deep RAM Purge complete. Freed {collected} dead objects.", flush=True)
            except Exception as e:
                print(f"⚠️ [Memory Engine] Purge failed: {e}", flush=True)

# 🛑 PASTE IT RIGHT HERE AT THE ABSOLUTE BOTTOM OF THE CLASS 🛑
    async def close(self):
        if self.raw_session:
            await self.raw_session.close()
        await super().close()
                
# 4. Master Engine Initialization
async def main():
    raw_tokens = os.environ.get('BOT_TOKENS')
    if not raw_tokens:
        print("❌ ERROR: No BOT_TOKENS found in Render Environment Variables!", flush=True)
        return

    token_list = [t.strip() for t in raw_tokens.split(',') if t.strip()]
    clients = []

    print(f"⚡ Initializing multi-token array with {len(token_list)} targets...", flush=True)

    # Create a shielded login function so dead tokens don't crash the good ones
    async def safe_start(client, token):
        try:
            await client.start(token)
        except Exception as e:
            print(f"💀 DEAD TOKEN SKIPPED [{token[:10]}...]: {e}", flush=True)

    # Build client instances for every token
    for i, token in enumerate(token_list):
        client = ForbidToken()
        clients.append(safe_start(client, token))
        
        if i < len(token_list) - 1:
            # FAST_BOOT = True gives a safe minimum 1s delay locally.
            # FAST_BOOT = False gives the full 15s+ IP cloak for Railway production.
            boot_delay = 1.0 if FAST_BOOT else (15.0 + random.uniform(1.0, 5.0))
            print(f"⏳ [System] Holding next token for {boot_delay:.1f}s...", flush=True)
            await asyncio.sleep(boot_delay)

    # Fire all connections concurrently (they are already mathematically spaced out now!)
    print("🚀 Firing connections concurrently...", flush=True)
    await asyncio.gather(*clients)
    
if __name__ == "__main__":
    # 1. Start the web server in the background ONLY after everything is loaded
    keep_alive()
    
    # 2. Ignite the botnet
    asyncio.run(main())
