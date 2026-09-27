import os
import streamlit as st
import streamlit.components.v1 as components

from modules.ai_engine import ask_agrisense_stream, build_farm_context


def show_live_voice():
    farmer = st.session_state.get("farmer")

    if not farmer:
        st.warning("Please login first.")
        return

    language = st.session_state.get(
        "selected_language",
        farmer.get("language", "English")
    )

    bcp47_codes = {
        "English": "en-IN",
        "తెలుగు": "te-IN",
        "हिंदी": "hi-IN",
        "தமிழ்": "ta-IN",
        "ಕನ್ನಡ": "kn-IN",
        "मराठी": "mr-IN",
    }

    speech_lang = bcp47_codes.get(language, "en-IN")
    farmer_id = farmer["id"]

    # Header Card
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #15803d 0%, #166534 100%); color: white; padding: 22px; border-radius: 18px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="color: white; margin: 0; font-size: 22px; font-weight: 800;">🎙️ AgriSense Multilingual Voice AI</h2>
                    <p style="color: #dcfce7; margin: 6px 0 0 0; font-size: 13px;">👨‍🌾 {farmer['name']} &nbsp;•&nbsp; 🌐 Language: <strong>{language}</strong></p>
                </div>
                <div style="font-size: 34px;">🌾</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_back, col_info = st.columns([1, 3])
    with col_back:
        if st.button("⬅️ Back to Chat", key="btn_back_ai", use_container_width=True):
            st.session_state.page = "voice"
            st.rerun()

    with col_info:
        st.caption("💡 Speak naturally in your native language. AgriSense AI knows your soil, weather, and crop recommendations.")

    st.markdown("---")

    # Tabs for both Real-Time WebSocket Voice and Direct In-Browser Voice
    tab_live, tab_browser = st.tabs([
        "⚡ Real-Time Streaming (Gemini Live WebSocket)",
        "🎙️ Direct Browser Voice (Zero Server Setup)"
    ])

    with tab_live:
        st.markdown(
            """
            <div style="font-size: 13px; color: #475569; margin-bottom: 8px;">
                Connects to the low-latency Gemini Live WebSocket backend on <code>localhost:8000/live</code>.
            </div>
            """,
            unsafe_allow_html=True
        )

        html_live_voice = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                * {{
                    box-sizing: border-box;
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                }}
                body {{
                    margin: 0;
                    padding: 10px;
                    background: transparent;
                    text-align: center;
                }}
                .voice-card {{
                    max-width: 620px;
                    margin: auto;
                    padding: 24px;
                    border-radius: 20px;
                    background: #ffffff;
                    border: 1.5px solid #e2e8f0;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
                }}
                .server-status {{
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    padding: 6px 14px;
                    border-radius: 999px;
                    font-size: 13px;
                    font-weight: 700;
                    margin-bottom: 14px;
                }}
                .server-online {{
                    background: #dcfce7;
                    color: #15803d;
                }}
                .server-offline {{
                    background: #fee2e2;
                    color: #b91c1c;
                }}
                .pulse-ring {{
                    display: none;
                    width: 72px;
                    height: 72px;
                    margin: 12px auto;
                    border-radius: 50%;
                    background: #22c55e;
                    animation: pulse 1.5s infinite;
                }}
                @keyframes pulse {{
                    0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }}
                    70% {{ transform: scale(1.05); box-shadow: 0 0 0 16px rgba(34, 197, 94, 0); }}
                    100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }}
                }}
                .btn-row {{
                    display: flex;
                    gap: 12px;
                    justify-content: center;
                    margin: 18px 0;
                }}
                button {{
                    flex: 1;
                    max-width: 240px;
                    padding: 14px 20px;
                    border: none;
                    border-radius: 12px;
                    font-size: 16px;
                    font-weight: 700;
                    cursor: pointer;
                    transition: all 0.2s ease;
                }}
                #startBtn {{
                    background: #16a34a;
                    color: white;
                    box-shadow: 0 4px 12px rgba(22, 163, 74, 0.3);
                }}
                #startBtn:hover {{
                    background: #15803d;
                }}
                #stopBtn {{
                    background: #dc2626;
                    color: white;
                    box-shadow: 0 4px 12px rgba(220, 38, 38, 0.25);
                }}
                #stopBtn:hover {{
                    background: #b91c1c;
                }}
                #statusText {{
                    font-size: 15px;
                    font-weight: 700;
                    color: #334155;
                    margin: 12px 0;
                    min-height: 24px;
                }}
                .transcript-box {{
                    min-height: 100px;
                    max-height: 200px;
                    overflow-y: auto;
                    padding: 16px;
                    border-radius: 14px;
                    background: #f8fafc;
                    border: 1.5px solid #e2e8f0;
                    text-align: left;
                    font-size: 15px;
                    line-height: 1.5;
                    color: #0f172a;
                }}
                .offline-alert {{
                    display: none;
                    margin-top: 14px;
                    padding: 12px;
                    background: #fff7ed;
                    border: 1.5px solid #fed7aa;
                    border-radius: 12px;
                    color: #9a3412;
                    font-size: 13px;
                    text-align: left;
                }}
            </style>
        </head>
        <body>
            <div class="voice-card">
                <div id="serverBadge" class="server-status server-offline">
                    <span>Checking server (port 8000)...</span>
                </div>

                <div id="pulseCircle" class="pulse-ring"></div>

                <div id="statusText">⚪ Ready to connect</div>

                <div class="btn-row">
                    <button id="startBtn">🎤 Start Speaking</button>
                    <button id="stopBtn" disabled style="opacity: 0.6;">⏹ Stop</button>
                </div>

                <div style="text-align: left; font-size: 13px; font-weight: 700; color: #64748b; margin-bottom: 6px;">
                    AI Voice Response & Transcript:
                </div>
                <div id="transcriptBox" class="transcript-box">
                    Click "Start Speaking" and talk to AgriSense AI...
                </div>

                <div id="offlineAlert" class="offline-alert">
                    <strong>⚠️ Server Offline:</strong> Live Voice WebSocket server is not running on <code>localhost:8000</code>.<br>
                    To start it, open your terminal and run:
                    <pre style="background: #ffffff; padding: 6px 10px; border-radius: 6px; margin: 6px 0 0 0; font-family: monospace;">python server.py</pre>
                </div>
            </div>

            <script>
            const farmerId = "{farmer_id}";
            const language = "{language}";
            const backendHost = window.location.hostname || "localhost";
            const httpUrl = "http://" + backendHost + ":8000/health";
            const wsProtocol = window.location.protocol === "https:" ? "wss:" : "ws:";
            const wsUrl = wsProtocol + "//" + backendHost + ":8000/live?language=" + encodeURIComponent(language) + "&farmer_id=" + encodeURIComponent(farmerId);

            let websocket = null;
            let audioContext = null;
            let processor = null;
            let microphone = null;
            let stream = null;
            let playbackCtx = null;
            let nextStartTime = 0;
            let userStopped = false;
            let serverIsOnline = false;

            const serverBadge = document.getElementById("serverBadge");
            const offlineAlert = document.getElementById("offlineAlert");
            const statusText = document.getElementById("statusText");
            const transcriptBox = document.getElementById("transcriptBox");
            const startBtn = document.getElementById("startBtn");
            const stopBtn = document.getElementById("stopBtn");
            const pulseCircle = document.getElementById("pulseCircle");

            async function checkServerHealth() {{
                try {{
                    const res = await fetch(httpUrl, {{ mode: "cors", cache: "no-store" }});
                    if (res.ok) {{
                        serverIsOnline = true;
                        serverBadge.className = "server-status server-online";
                        serverBadge.innerHTML = "🟢 Live WebSocket Server Online (Port 8000)";
                        offlineAlert.style.display = "none";
                    }} else {{
                        throw new Error("Bad status");
                    }}
                }} catch (e) {{
                    serverIsOnline = false;
                    serverBadge.className = "server-status server-offline";
                    serverBadge.innerHTML = "🔴 WebSocket Server Offline (Port 8000)";
                    offlineAlert.style.display = "block";
                }}
            }}

            checkServerHealth();
            setInterval(checkServerHealth, 6000);

            function downsample(buffer, inputSampleRate, outputSampleRate) {{
                if (outputSampleRate === inputSampleRate) return buffer;
                const sampleRateRatio = inputSampleRate / outputSampleRate;
                const newLength = Math.round(buffer.length / sampleRateRatio);
                const result = new Float32Array(newLength);
                let offsetResult = 0;
                let offsetBuffer = 0;
                while (offsetResult < result.length) {{
                    const nextOffsetBuffer = Math.round((offsetResult + 1) * sampleRateRatio);
                    let accum = 0;
                    let count = 0;
                    for (let i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {{
                        accum += buffer[i];
                        count++;
                    }}
                    result[offsetResult] = count ? accum / count : 0;
                    offsetResult++;
                    offsetBuffer = nextOffsetBuffer;
                }}
                return result;
            }}

            function floatTo16BitPCM(float32Array) {{
                const buffer = new ArrayBuffer(float32Array.length * 2);
                const view = new DataView(buffer);
                let offset = 0;
                for (let i = 0; i < float32Array.length; i++, offset += 2) {{
                    let sample = Math.max(-1, Math.min(1, float32Array[i]));
                    view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
                }}
                return buffer;
            }}

            function playAudioChunk(audioData) {{
                try {{
                    if (!playbackCtx || playbackCtx.state === "closed") {{
                        playbackCtx = new (window.AudioContext || window.webkitAudioContext)({{ sampleRate: 24000 }});
                    }}
                    if (playbackCtx.state === "suspended") {{
                        playbackCtx.resume();
                    }}
                    const int16 = new Int16Array(audioData);
                    const audioBuffer = playbackCtx.createBuffer(1, int16.length, 24000);
                    const channel = audioBuffer.getChannelData(0);
                    for (let i = 0; i < int16.length; i++) {{
                        channel[i] = int16[i] / 32768;
                    }}
                    const source = playbackCtx.createBufferSource();
                    source.buffer = audioBuffer;
                    source.connect(playbackCtx.destination);

                    const now = playbackCtx.currentTime;
                    if (nextStartTime < now) {{
                        nextStartTime = now;
                    }}
                    source.start(nextStartTime);
                    nextStartTime += audioBuffer.duration;
                }} catch (err) {{
                    console.error("Audio playback error:", err);
                }}
            }}

            async function startVoice() {{
                try {{
                    userStopped = false;
                    nextStartTime = 0;
                    statusText.innerText = "🟡 Connecting to AgriSense AI...";
                    startBtn.disabled = true;
                    stopBtn.disabled = false;
                    stopBtn.style.opacity = "1";

                    websocket = new WebSocket(wsUrl);
                    websocket.binaryType = "arraybuffer";

                    websocket.onopen = async () => {{
                        statusText.innerText = "🟢 Connected — Speak naturally now";
                        pulseCircle.style.display = "block";
                        transcriptBox.innerText = "Listening to your voice...";

                        stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                        audioContext = new (window.AudioContext || window.webkitAudioContext)();
                        microphone = audioContext.createMediaStreamSource(stream);
                        processor = audioContext.createScriptProcessor(4096, 1, 1);

                        processor.onaudioprocess = function(event) {{
                            if (!websocket || websocket.readyState !== WebSocket.OPEN) return;
                            const input = event.inputBuffer.getChannelData(0);
                            const downsampled = downsample(input, audioContext.sampleRate, 16000);
                            const pcm = floatTo16BitPCM(downsampled);
                            websocket.send(pcm);
                        }};

                        microphone.connect(processor);
                        const muteGain = audioContext.createGain();
                        muteGain.gain.value = 0;
                        processor.connect(muteGain);
                        muteGain.connect(audioContext.destination);
                    }};

                    websocket.onmessage = async (event) => {{
                        if (typeof event.data === "string") {{
                            if (event.data.startsWith("AI_TEXT:")) {{
                                const text = event.data.substring(8);
                                transcriptBox.innerText = text;
                            }} else if (event.data === "AI_DONE") {{
                                statusText.innerText = "🟢 AgriSense finished speaking";
                            }} else if (event.data.startsWith("ERROR:")) {{
                                const err = event.data.substring(6);
                                statusText.innerText = "🔴 Server Error: " + err;
                                transcriptBox.innerText = "⚠️ " + err;
                            }}
                            return;
                        }}
                        if (event.data instanceof ArrayBuffer) {{
                            playAudioChunk(event.data);
                        }}
                    }};

                    websocket.onerror = (error) => {{
                        console.error("WebSocket error:", error);
                        statusText.innerText = "🔴 Connection error (Server offline or unreachable)";
                        offlineAlert.style.display = "block";
                    }};

                    websocket.onclose = (event) => {{
                        console.log("WebSocket closed:", event.code, event.reason);
                        pulseCircle.style.display = "none";
                        startBtn.disabled = false;
                        stopBtn.disabled = true;
                        stopBtn.style.opacity = "0.6";

                        if (userStopped || event.code === 1000) {{
                            statusText.innerText = "⏹ Voice session ended";
                        }} else if (event.code === 1005 || event.code === 1006) {{
                            statusText.innerText = "🔴 Disconnected: WebSocket Server is not running on port 8000";
                            offlineAlert.style.display = "block";
                        }} else {{
                            statusText.innerText = "🔴 Closed (" + event.code + (event.reason ? ": " + event.reason : "") + ")";
                        }}
                    }};

                }} catch (error) {{
                    console.error("Start voice error:", error);
                    statusText.innerText = "🔴 Microphone permission denied or browser error";
                    startBtn.disabled = false;
                    stopBtn.disabled = true;
                    stopBtn.style.opacity = "0.6";
                }}
            }}

            function stopVoice() {{
                userStopped = true;
                if (processor) {{ processor.disconnect(); processor = null; }}
                if (microphone) {{ microphone.disconnect(); microphone = null; }}
                if (stream) {{ stream.getTracks().forEach(t => t.stop()); stream = null; }}
                if (audioContext) {{ audioContext.close(); audioContext = null; }}
                if (playbackCtx) {{ playbackCtx.close(); playbackCtx = null; }}
                if (websocket) {{ websocket.close(1000, "User stopped"); websocket = null; }}
                pulseCircle.style.display = "none";
                statusText.innerText = "⏹ Voice stopped";
                startBtn.disabled = false;
                stopBtn.disabled = true;
                stopBtn.style.opacity = "0.6";
            }}

            startBtn.onclick = startVoice;
            stopBtn.onclick = stopVoice;
            </script>
        </body>
        </html>
        """

        components.html(html_live_voice, height=520, scrolling=False)

    with tab_browser:
        st.markdown(
            f"""
            <div style="background: #f1f5f9; padding: 14px; border-radius: 12px; margin-bottom: 14px; font-size: 13px; color: #334155;">
                ✨ <strong>Zero-Setup Mode:</strong> Uses your browser's native Speech Recognition & Text-to-Speech in <strong>{language} ({speech_lang})</strong> directly connected to AgriSense AI. Works on all modern browsers without running any backend servers.
            </div>
            """,
            unsafe_allow_html=True
        )

        farm_ctx, crop_ctx = build_farm_context(farmer_id)

        # In-browser speech recognition and synthesis widget
        html_browser_voice = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                * {{ box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
                body {{ margin: 0; padding: 10px; background: transparent; text-align: center; }}
                .card {{
                    max-width: 620px;
                    margin: auto;
                    padding: 24px;
                    border-radius: 20px;
                    background: #ffffff;
                    border: 1.5px solid #cbd5e1;
                    box-shadow: 0 4px 18px rgba(0,0,0,0.06);
                }}
                .mic-btn {{
                    width: 90px;
                    height: 90px;
                    border-radius: 50%;
                    border: none;
                    background: linear-gradient(135deg, #15803d, #22c55e);
                    color: white;
                    font-size: 36px;
                    cursor: pointer;
                    margin: 14px auto;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    box-shadow: 0 6px 18px rgba(34, 197, 94, 0.35);
                    transition: all 0.2s ease;
                }}
                .mic-btn.listening {{
                    background: linear-gradient(135deg, #dc2626, #ef4444);
                    animation: pulse-red 1.2s infinite;
                }}
                @keyframes pulse-red {{
                    0% {{ transform: scale(0.96); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }}
                    70% {{ transform: scale(1.08); box-shadow: 0 0 0 16px rgba(239, 68, 68, 0); }}
                    100% {{ transform: scale(0.96); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
                }}
                .status {{
                    font-size: 16px;
                    font-weight: 700;
                    color: #1e293b;
                    margin: 10px 0;
                }}
                .box {{
                    text-align: left;
                    padding: 14px;
                    border-radius: 12px;
                    background: #f8fafc;
                    border: 1.5px solid #e2e8f0;
                    margin-top: 12px;
                    font-size: 14px;
                    line-height: 1.5;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <button id="micBtn" class="mic-btn">🎙️</button>
                <div id="bStatus" class="status">Tap microphone and ask your farming question in {language}</div>

                <div style="display: flex; gap: 8px; justify-content: center; margin: 10px 0;">
                    <button id="stopSpeakBtn" style="padding: 8px 16px; border-radius: 8px; border: 1px solid #cbd5e1; background: #fff; cursor: pointer; font-size: 13px; font-weight: 600;">
                        ⏹ Stop AI Voice
                    </button>
                </div>

                <div class="box">
                    <div style="font-size: 12px; font-weight: 700; color: #64748b; margin-bottom: 4px;">👨‍🌾 You Said:</div>
                    <div id="userSpeech" style="color: #0f172a; font-weight: 600; min-height: 22px;">...</div>
                </div>

                <div class="box">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-size: 12px; font-weight: 700; color: #15803d;">🤖 AgriSense AI Response:</span>
                        <span id="aiStatus" style="font-size: 11px; color: #64748b;">Ready</span>
                    </div>
                    <div id="aiReply" style="color: #0f172a; min-height: 50px;">Your advice will appear and be spoken aloud here...</div>
                </div>
            </div>

            <script>
            const speechLang = "{speech_lang}";
            const languageName = "{language}";
            const farmerId = "{farmer_id}";

            const micBtn = document.getElementById("micBtn");
            const bStatus = document.getElementById("bStatus");
            const userSpeech = document.getElementById("userSpeech");
            const aiReply = document.getElementById("aiReply");
            const aiStatus = document.getElementById("aiStatus");
            const stopSpeakBtn = document.getElementById("stopSpeakBtn");

            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            let recognition = null;
            let isListening = false;
            let synth = window.speechSynthesis;

            if (SpeechRecognition) {{
                recognition = new SpeechRecognition();
                recognition.lang = speechLang;
                recognition.interimResults = false;
                recognition.maxAlternatives = 1;

                recognition.onstart = () => {{
                    isListening = true;
                    micBtn.classList.add("listening");
                    bStatus.innerText = "🔴 Listening in " + languageName + "... Speak now!";
                }};

                recognition.onresult = async (event) => {{
                    const query = event.results[0][0].transcript;
                    userSpeech.innerText = query;
                    bStatus.innerText = "⏳ Thinking & consulting farm data...";
                    aiStatus.innerText = "Generating...";
                    aiReply.innerText = "Consulting AgriSense AI...";

                    // Query backend AI API
                    try {{
                        const backendHost = window.location.hostname || "localhost";
                        const response = await fetch("http://" + backendHost + ":8000/ai/ask", {{
                            method: "POST",
                            headers: {{ "Content-Type": "application/json" }},
                            body: JSON.stringify({{
                                farmer_id: parseInt(farmerId),
                                question: query,
                                language: languageName
                            }})
                        }});

                        if (response.ok) {{
                            const data = await response.json();
                            const answer = data.answer || "No response received.";
                            aiReply.innerText = answer;
                            aiStatus.innerText = "Speaking...";
                            bStatus.innerText = "🟢 AgriSense is responding";
                            speakText(answer, speechLang);
                        }} else {{
                            throw new Error("Server response not ok");
                        }}
                    }} catch (e) {{
                        console.warn("FastAPI query failed, fallback prompt to user:", e);
                        aiReply.innerText = "Note: To enable direct voice query, ensure 'python server.py' is running, or ask directly in the AI Chat tab!";
                        bStatus.innerText = "⚠️ Voice transcribed! Please view AI Chat or start server.";
                    }}
                }};

                recognition.onerror = (event) => {{
                    console.error("Speech recognition error:", event.error);
                    bStatus.innerText = "❌ Speech error: " + event.error + " (Tap mic to try again)";
                    micBtn.classList.remove("listening");
                    isListening = false;
                }};

                recognition.onend = () => {{
                    micBtn.classList.remove("listening");
                    isListening = false;
                    if (!bStatus.innerText.includes("Thinking")) {{
                        bStatus.innerText = "Tap microphone to speak again";
                    }}
                }};
            }} else {{
                bStatus.innerText = "⚠️ Web Speech is not supported in this browser. Please use Chrome/Edge.";
            }}

            function speakText(text, lang) {{
                if (!synth) return;
                synth.cancel();
                // Clean markdown symbols for cleaner TTS
                const clean = text.replace(/[*#_`]/g, "");
                const utterance = new SpeechSynthesisUtterance(clean);
                utterance.lang = lang;
                utterance.rate = 1.0;
                utterance.onend = () => {{
                    aiStatus.innerText = "Finished speaking";
                    bStatus.innerText = "Tap microphone to speak again";
                }};
                synth.speak(utterance);
            }}

            micBtn.onclick = () => {{
                if (!recognition) {{
                    alert("Speech Recognition not supported in this browser. Please use Chrome or Edge.");
                    return;
                }}
                if (synth) synth.cancel();
                if (isListening) {{
                    recognition.stop();
                }} else {{
                    recognition.start();
                }}
            }};

            stopSpeakBtn.onclick = () => {{
                if (synth) synth.cancel();
                aiStatus.innerText = "Voice stopped";
                bStatus.innerText = "Tap microphone to speak again";
            }};
            </script>
        </body>
        </html>
        """

        components.html(html_browser_voice, height=480, scrolling=False)