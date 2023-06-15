

let wsStart = "ws://";
const loc = window.location;
if(loc.protocol === "https:") {
    wsStart = "wss://";
}
const endpoint = wsStart + loc.host + "/" + ROOM_ID + "/" + username;
console.log(endpoint, "endpoint");
const websocket = new WebSocket(endpoint);

let mapPeers= {};



// WebSocket Methods

websocket.onopen = (e) => {
    console.log("Open", e);
    sendSignal('new-peer', {});
};

websocket.onmessage = (e) => {
    console.log("Message", e);
    const data = JSON.parse(e.data);
    if(data['action'] == 'new-message'){
        createMessage(data);
    }
    else{
        signalMessage(data);
    }
    
};

websocket.onclose = (e) => {
    console.log("Close", e);
};

websocket.onerror = (e) => {
    console.log("Error", e);
};

const sendMessage = () => {
    const message = document.querySelector("#msg-input");
    websocket.send(JSON.stringify({
        "username" : username,
        "action" : "new-message",
        "message": message.value
    }));
    message.value = "";
}

const sendSignal = (action, message) => {
    websocket.send(JSON.stringify({
        "username" : username,
        "action" : action,
        "message": message,
    }))
};

document.querySelector("#msg-input").addEventListener("keyup", (e) => {
    if(e.keyCode === 13) {
        sendMessage();
    }
});

// Video Function
let localStream = new MediaStream();
const constraints = {
    "video" : true,
    "audio" : true,
};

const mainVideos = document.querySelector("#videoGrid");
const audioBtn = document.querySelector("#mute-btn");
const videoBtn = document.querySelector("#video-btn");

let userMedia = navigator.mediaDevices.getUserMedia(constraints)
    .then(stream => {
        localStream = stream;
        localVideo = document.createElement("video");
        localVideo.classList.add("mainVideos__video");
        localVideo.srcObject = localStream;
        localVideo.muted = true;
        localVideo.addEventListener("loadedmetadata", () => {
            localVideo.play();
        });
        mainVideos.appendChild(localVideo);
        let audioTracks = stream.getAudioTracks();
        let videoTracks = stream.getVideoTracks();
    
        audioTracks[0].enabled = true;
        videoTracks[0].enabled = true;

        audioBtn.addEventListener("click", () => {
            if(audioTracks[0].enabled) {
                audioTracks[0].enabled = false;
                document.querySelector("#mute-btn>span").innerHTML = "Audio On";
            }
            else{
                audioTracks[0].enabled = true;
                document.querySelector("#mute-btn>span").innerHTML = "Audio Off";
            }
        });

        videoBtn.addEventListener("click", () => {
            if(videoTracks[0].enabled) {
                videoTracks[0].enabled = false;
                document.querySelector("#video-btn>span").innerHTML = "Video On";
            }
            else{
                videoTracks[0].enabled = true;
                document.querySelector("#video-btn>span").innerHTML = "Video Off";
            }
        });
    })
    .catch(e => {
        console.log("error", e);
    })

// Message Fuction 

const createMessage = (data) => {
    const message = data.message;
    if(message === ""){
        return;
    }
    let user = data.username;
    if(user == username) {
        user = "Me"
    }
    const msgContainer = document.querySelector(".mainChatWindow");
    const newMessage = document.createElement("div");
    newMessage.classList.add("message");
    newMessage.innerHTML = `<div class="message__user">${user} : </div><div class="message__text"> ${message}</div>`;
    msgContainer.appendChild(newMessage);
    msgContainer.scrollTop = msgContainer.scrollHeight;
}

const signalMessage = (data) => {
    let peerUser = data['username'];
    let action = data['action'];

    if(peerUser == username) {
        return;
    }
    let receiverChannelName = data['message']['receiver_channel_name'];

    if(action == 'new-peer') {
        createOfferer(peerUser, receiverChannelName);
        return;
    }

    if(action == 'new-offer') {
        let offer = data['message']['sdp'];
        createAnswerer(offer, peerUser, receiverChannelName);
        return;
    }

    if(action == 'new-answer') {
        let answer = data['message']['sdp'];
        let peer = mapPeers[peerUser][0];
        peer.setRemoteDescription(answer);
        return;
    }

}


// WebRTC Function

const createOfferer = (peerUser, receiverChannelName) => {
    let peer = new RTCPeerConnection(null);
    addLocalTracks(peer);

    let dc = peer.createDataChannel("channel");
    dc.addEventListener("open", () => {
        console.log("Connection opened");
    });

    let remoteVideo = createVideo(peerUser);
    setOnTrack(peer, remoteVideo);

    mapPeers[peerUser] = [peer, dc];

    peer.addEventListener("iceconnectionstatechange", () => {
        let iceConnectionState = peer.iceConnectionState;
        if(iceConnectionState === "failed" || iceConnectionState === "disconnected" || iceConnectionState === "closed") {
            console.log("Closing connection");
            delete mapPeers[peerUser];
            if(iceConnectionState != "closed") {
                peer.close();
            }
            removeVideo(remoteVideo);
        }
    });

    peer.addEventListener("icecandidate", (event) => {
        if(event.candidate) {
            console.log("New ice candidate", JSON.stringify(peer.localDescription));
            return;
        }
        sendSignal("new-offer", {
            "sdp" : peer.localDescription,
            "receiver_channel_name" : receiverChannelName,
        });
    });
    peer.createOffer()
        .then(o => peer.setLocalDescription(o))
        .then(() => {
            console.log("Local description set successfully");
        })
}

const addLocalTracks = (peer) => {
    localStream.getTracks().forEach(track => {
        peer.addTrack(track, localStream);
    })
}

const createVideo = (peerUser) => {
    let remoteVideo = document.createElement("video");
    remoteVideo.classList.add("mainVideos__video");
    remoteVideo.setAttribute("id", peerUser);
    remoteVideo.autoplay = true;
    remoteVideo.playsinline = true;
    mainVideos.appendChild(remoteVideo);
    return remoteVideo;
};

const setOnTrack = (peer, remoteVideo) => {
    let remoteStream = new MediaStream();
    remoteVideo.srcObject = remoteStream;
    peer.addEventListener("track", async (event) => {
        remoteStream.addTrack(event.track, remoteStream);
    })
}

const removeVideo = (video) => {
    let videoWrapper = video.parentNode;

    videoWrapper.removeChild(video);
}

const createAnswerer = (offer, peerUser, receiverChannelName) => {
    let peer = new RTCPeerConnection(null);
    addLocalTracks(peer);

    let remoteVideo = createVideo(peerUser);
    setOnTrack(peer, remoteVideo);

    peer.addEventListener("datachannel", (event) => {
        peer.dc = event.channel;
        peer.dc.addEventListener("open", () => {
            console.log("Connection opened");
        });

        mapPeers[peerUser] = [peer, peer.dc];
    });

    peer.addEventListener("iceconnectionstatechange", () => {
        let iceConnectionState = peer.iceConnectionState;
        if(iceConnectionState === "failed" || iceConnectionState === "disconnected" || iceConnectionState === "closed") {
            console.log("Closing connection");
            delete mapPeers[peerUser];
            if(iceConnectionState != "closed") {
                peer.close();
            }
            removeVideo(remoteVideo);
        }
    });

    peer.addEventListener("icecandidate", (event) => {
        if(event.candidate) {
            console.log("New ice candidate", JSON.stringify(peer.localDescription));
            return;
        }
        sendSignal("new-answer", {
            "sdp" : peer.localDescription,
            "receiver_channel_name" : receiverChannelName,
        });
    });
    peer.setRemoteDescription(offer)
        .then(()=> {
            console.log("Remote description set successfully for %s",peerUser);
            return peer.createAnswer();
        })
        .then(a => {
            console.log("Answer Created!");
            peer.setLocalDescription(a);
        })
}

document.querySelector("#endnow").addEventListener("click", () => {
    window.location.href = "http://localhost:8000/";
});