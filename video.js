// 高级控制参数（可调节）
const playbackConfig = {
    normalSpeed: 1.0,     // 正序播放速度
    reverseSpeed: 1.0,    // 倒序播放速度
    transition: {
        duration: 0.5,    // 过渡动画时长（秒）
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)' // 缓动函数
    }
};

// 添加过渡动画
function applyTransition() {
    video.style.transition = `all ${playbackConfig.transition.duration}s ${playbackConfig.transition.easing}`;
    setTimeout(() => video.style.transition = '', playbackConfig.transition.duration * 1000);
}

// 增强版倒放控制器
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