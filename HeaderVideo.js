const playbackConfig = {
    normalSpeed: 1.0,     
    reverseSpeed: 1.0,   
    transition: {
        duration: 0.5,    
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)' 
    }
};

function applyTransition() {
    video.style.transition = `all ${playbackConfig.transition.duration}s ${playbackConfig.transition.easing}`;
    setTimeout(() => video.style.transition = '', playbackConfig.transition.duration * 1000);
}

function enhancedReversePlay() {
    const frame = () => {
        const currentTime = video.currentTime;
        const targetTime = Math.max(0, currentTime - (timeStep * playbackConfig.reverseSpeed));
        
        if (targetTime > 0) {
            video.currentTime = targetTime;
            requestAnimationFrame(frame);
        } else {
            video.currentTime = 0;
            applyTransition();
            handleReverseEnd();
        }
    }
    requestAnimationFrame(frame);
}