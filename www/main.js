$(document).ready(function () {

    // ══════════════════════════════════════════════════════════
    //  AUTO-DETECT SERVER URL
    //  Works both locally (localhost:5000) and on Render/web
    // ══════════════════════════════════════════════════════════
    var FLASK = window.location.origin;  // same domain always

    // ══════════════════════════════════════════════════════════
    //  CONFIG
    // ══════════════════════════════════════════════════════════
    var cfg = {
        lang:     'en-IN',
        timeout:  5000,
        userName: "there",
        voicePref:'female'
    };

    // ══════════════════════════════════════════════════════════
    //  SPLASH — 2.5s then show app
    // ══════════════════════════════════════════════════════════
    setTimeout(function () {
        $("#Splash").addClass("out");
        setTimeout(function () {
            $("#Splash").hide();
            $("#App").removeAttr("hidden");
            pingServer();
            setGreeting();
        }, 600);
    }, 2500);

    // ══════════════════════════════════════════════════════════
    //  CLOCK
    // ══════════════════════════════════════════════════════════
    function tickClock() {
        var n = new Date(), h = n.getHours(), m = n.getMinutes();
        var ap = h >= 12 ? "PM" : "AM"; h = h % 12 || 12;
        $("#TopClock").text(String(h).padStart(2,"0") + ":" + String(m).padStart(2,"0") + " " + ap);
    }
    tickClock(); setInterval(tickClock, 10000);

    // ══════════════════════════════════════════════════════════
    //  GREETING
    // ══════════════════════════════════════════════════════════
    function setGreeting() {
        var h = new Date().getHours();
        var g = h < 12 ? "Good Morning" : h < 17 ? "Good Afternoon" : "Good Evening";
        $("#HomeGreeting").text(g);
    }

    // ══════════════════════════════════════════════════════════
    //  SETTINGS
    // ══════════════════════════════════════════════════════════
    $("#SettingsBtn").click(function () { $("#SettingsOverlay, #SettingsPanel").fadeIn(200); });
    $("#SettingsOverlay").click(function () { $("#SettingsOverlay, #SettingsPanel").fadeOut(200); });
    $("#SaveSettings").click(function () {
        cfg.lang      = $("#LangSelect").val();
        cfg.userName  = $("#UserName").val() || "there";
        cfg.voicePref = $("#VoiceSelect").val();
        setGreeting();
        $("#SettingsOverlay, #SettingsPanel").fadeOut(200);
    });

    $("#HistoryBtn").click(function () {
        new bootstrap.Offcanvas(document.getElementById("HistoryPanel")).show();
    });

    // ══════════════════════════════════════════════════════════
    //  CHIPS
    // ══════════════════════════════════════════════════════════
    $(".chip").on("click", function () {
        $("#chatbox").val($(this).data("q"));
        sendFromInput("chatbox");
    });

    // ══════════════════════════════════════════════════════════
    //  INPUT BINDING
    // ══════════════════════════════════════════════════════════
    bindInput("chatbox",  "SendBtn",  "MicBtn");
    bindInput("chatbox2", "SendBtn2", "MicBtn2");

    function bindInput(taId, sendId, micId) {
        $("#" + taId).on("input", function () {
            this.style.height = "auto";
            this.style.height = Math.min(this.scrollHeight, 130) + "px";
            var has = $(this).val().trim() !== "";
            $("#" + sendId).attr("hidden", !has || null);
            $("#" + micId).attr("hidden",  has  || null);
        }).on("keydown", function (e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault(); sendFromInput(taId);
            }
        });
        $("#" + sendId).on("click", function () { sendFromInput(taId); });
        $("#" + micId).on("click",  function () {
            activeMicId = micId; activeBoxId = taId;
            recognizing ? commitVoice() : startVoice();
        });
    }

    function sendFromInput(taId) {
        var text = $("#" + taId).val().trim();
        if (!text) return;
        $("#" + taId).val("").css("height", "auto").trigger("input");
        sendToServer(text);
    }

    $("#HomeBtn").on("click", showHome);

    // ══════════════════════════════════════════════════════════
    //  VIEWS
    // ══════════════════════════════════════════════════════════
    function showHome() {
        $("#ChatView").attr("hidden", true);
        $("#HomeView").removeClass("out");
        $("#ChatScroll").empty();
    }
    function showChat() {
        $("#HomeView").addClass("out");
        setTimeout(function () { $("#ChatView").removeAttr("hidden"); }, 250);
    }

    // ══════════════════════════════════════════════════════════
    //  VOICE
    // ══════════════════════════════════════════════════════════
    var recognizing = false, recognition = null;
    var silTimer = null, voiceText = "";
    var activeMicId = "MicBtn", activeBoxId = "chatbox";

    function startVoice() {
        var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SR) {
            addBubble("bot", "⚠️ Voice recognition requires Google Chrome or a Chromium browser.\nPlease type your command instead.");
            showChat(); return;
        }

        recognizing = true; voiceText = "";
        openVoiceOverlay();
        $("#" + activeMicId).addClass("recording");

        recognition = new SR();
        recognition.lang = cfg.lang;
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;

        recognition.onstart = function () {
            $("#VoHint").text("Speak clearly — auto-stops after 5 seconds of silence");
        };

        recognition.onresult = function (e) {
            var interim = "", final = "";
            for (var i = e.resultIndex; i < e.results.length; i++) {
                var t = e.results[i][0].transcript;
                if (e.results[i].isFinal) final += t; else interim += t;
            }
            voiceText += final;
            var display = (voiceText + interim).trim();
            $("#VoTranscript").text(display || "Listening...").toggleClass("active", display.length > 0);
            $("#" + activeBoxId).val(display);
            resetSilTimer();
        };

        recognition.onerror = function (e) {
            if (e.error === "no-speech") {
                $("#VoHint").text("Still listening...");
            } else if (e.error === "not-allowed") {
                closeVoiceOverlay(); stopVoice();
                addBubble("bot", "🎙️ Microphone blocked!\nClick the 🔒 icon in the address bar → Allow Microphone → Refresh.");
                showChat();
            } else if (e.error === "network") {
                closeVoiceOverlay(); stopVoice();
                $("#" + activeBoxId).attr("placeholder", "Voice unavailable — type here instead...").focus();
                setTimeout(function () { $("#chatbox,#chatbox2").attr("placeholder", "Ask me anything..."); }, 6000);
            }
        };

        recognition.onend = function () {
            if (recognizing) { try { recognition.start(); } catch(ex) {} }
        };

        recognition.start();
        resetSilTimer();
    }

    function resetSilTimer() {
        clearTimeout(silTimer);
        silTimer = setTimeout(commitVoice, cfg.timeout);
    }

    function commitVoice() {
        clearTimeout(silTimer);
        var text = voiceText.trim() || $("#" + activeBoxId).val().trim();
        closeVoiceOverlay(); stopVoice();
        if (text) {
            $("#" + activeBoxId).val(text).trigger("input");
            setTimeout(function () { sendFromInput(activeBoxId); }, 350);
        }
    }

    function stopVoice() {
        recognizing = false; clearTimeout(silTimer);
        $(".sb-mic").removeClass("recording");
        if (recognition) {
            recognition.onend = null;
            try { recognition.stop(); } catch(e) {}
            recognition = null;
        }
    }

    function openVoiceOverlay() {
        $("#VoTranscript").text("Listening...").removeClass("active");
        $("#VoHint").text("Speak clearly — auto-stops after 5 seconds of silence");
        $("#VoiceOverlay").removeAttr("hidden").hide().fadeIn(220);
    }
    function closeVoiceOverlay() {
        $("#VoiceOverlay").fadeOut(220, function () { $(this).attr("hidden", true); });
    }

    $("#StopVoiceBtn").on("click", commitVoice);

    // ══════════════════════════════════════════════════════════
    //  SEND TO SERVER
    // ══════════════════════════════════════════════════════════
    function sendToServer(text) {
        showChat();
        addBubble("user", text);
        var tid = addTyping();

        $.ajax({
            url:         FLASK + "/command",
            type:        "POST",
            contentType: "application/json",
            data:        JSON.stringify({ query: text, lang: cfg.lang }),
            timeout:     20000,

            success: function (data) {
                removeTyping(tid);
                var reply  = data.response || "Done.";
                var action = data.action;
                var url    = data.url;

                addBubble("bot", reply);
                browserSpeak(reply);
                addHistory(text);

                // If server wants to open a URL → open in new tab
                if (action === "open" && url) {
                    setTimeout(function () {
                        window.open(url, "_blank");
                    }, 800);
                }
            },

            error: function (xhr, status) {
                removeTyping(tid);
                if (xhr.status === 0) {
                    addBubble("bot", "❌ Cannot connect to server. Please refresh the page.");
                } else if (status === "timeout") {
                    addBubble("bot", "⚠️ Request timed out. Please try again.");
                } else {
                    addBubble("bot", "Server error " + xhr.status + ". Please try again.");
                }
            }
        });
    }

    // ══════════════════════════════════════════════════════════
    //  BUBBLES
    // ══════════════════════════════════════════════════════════
    function addBubble(who, text) {
        var t = new Date().toLocaleTimeString([], { hour:"2-digit", minute:"2-digit" });
        var html;
        if (who === "user") {
            html = '<div class="msg-row user">' +
                   '<div class="msg-bubble">' + esc(text) + '</div>' +
                   '<div class="msg-time">' + t + '</div></div>';
        } else {
            html = '<div class="msg-row bot">' +
                   '<div class="bot-label">' +
                   '<svg viewBox="0 0 40 40"><polygon class="hex-shape-sm" points="20,3 35,11 35,29 20,37 5,29 5,11"/>' +
                   '<text x="20" y="25" class="hex-letter-sm">N</text></svg>NOAH CYRUS</div>' +
                   '<div class="msg-bubble">' + esc(text) + '</div>' +
                   '<div class="msg-time">' + t + '</div></div>';
        }
        $("#ChatScroll").append(html);
        scrollDown();
    }

    var tcnt = 0;
    function addTyping() {
        var id = "td" + (++tcnt);
        $("#ChatScroll").append(
            '<div class="msg-row bot" id="' + id + '">' +
            '<div class="bot-label"><svg viewBox="0 0 40 40">' +
            '<polygon class="hex-shape-sm" points="20,3 35,11 35,29 20,37 5,29 5,11"/>' +
            '<text x="20" y="25" class="hex-letter-sm">N</text></svg>NOAH CYRUS</div>' +
            '<div class="msg-bubble typing-dots"><span></span><span></span><span></span></div></div>'
        );
        scrollDown(); return id;
    }
    function removeTyping(id) { $("#" + id).remove(); }
    function scrollDown() {
        var el = document.getElementById("ChatScroll");
        if (el) el.scrollTop = el.scrollHeight;
    }

    // ══════════════════════════════════════════════════════════
    //  HISTORY
    // ══════════════════════════════════════════════════════════
    function addHistory(text) {
        var t = new Date().toLocaleTimeString([], { hour:"2-digit", minute:"2-digit" });
        var p = text.length > 42 ? text.slice(0, 42) + "…" : text;
        $("#HistoryList").prepend(
            '<div class="hist-item"><div class="hist-q">' + esc(p) +
            '</div><div class="hist-t">' + t + '</div></div>'
        );
    }

    // ══════════════════════════════════════════════════════════
    //  BROWSER TTS
    // ══════════════════════════════════════════════════════════
    function browserSpeak(text) {
        if (!window.speechSynthesis) return;
        window.speechSynthesis.cancel();
        var u = new SpeechSynthesisUtterance(text);
        u.lang = cfg.lang; u.rate = 1.0; u.pitch = 1.0;
        var voices = window.speechSynthesis.getVoices();
        var pick = voices.find(function (v) {
            var n = v.name.toLowerCase();
            return v.lang.startsWith("en") && (cfg.voicePref === "female"
                ? (n.includes("zira") || n.includes("hazel") || n.includes("samantha") || n.includes("female"))
                : (n.includes("david") || n.includes("mark") || n.includes("male")));
        }) || voices.find(function (v) { return v.lang.startsWith("en"); });
        if (pick) u.voice = pick;
        window.speechSynthesis.speak(u);
    }

    // ══════════════════════════════════════════════════════════
    //  UTILS
    // ══════════════════════════════════════════════════════════
    function esc(s) {
        return String(s)
            .replace(/&/g,"&amp;").replace(/</g,"&lt;")
            .replace(/>/g,"&gt;").replace(/"/g,"&quot;")
            .replace(/\n/g,"<br>");
    }

    // ══════════════════════════════════════════════════════════
    //  PING SERVER
    // ══════════════════════════════════════════════════════════
    function pingServer() {
        $.ajax({
            url: FLASK + "/ping", type: "GET", timeout: 5000,
            success: function () {
                $("#StatusDot").removeClass("offline").addClass("online");
                $.getJSON(FLASK + "/greet", function (d) {
                    if (d.greeting) {
                        browserSpeak(d.greeting);
                        $("#HomeGreeting").text(d.greeting.split("!")[0]);
                    }
                });
            },
            error: function () {
                $("#StatusDot").removeClass("online").addClass("offline");
                addBubble("bot", "⚠️ Could not connect to NOAH CYRUS server.\nPlease refresh the page.");
                showChat();
            }
        });
    }

});
