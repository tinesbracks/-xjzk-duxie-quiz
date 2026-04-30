// 认证检查 - 在所有需要登录的页面中引入

// 检查登录状态
function checkAuth() {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    const loginTime = localStorage.getItem('loginTime');
    
    // 如果未登录，跳转到登录页面
    if (isLoggedIn !== 'true') {
        window.location.href = 'login.html';
        return false;
    }
    
    // 如果登录时间超过24小时，清除登录状态并跳转
    if (loginTime) {
        const currentTime = new Date().getTime();
        const timeDiff = currentTime - parseInt(loginTime);
        const hoursDiff = timeDiff / (1000 * 60 * 60);
        
        if (hoursDiff >= 24) {
            localStorage.removeItem('isLoggedIn');
            localStorage.removeItem('loginTime');
            window.location.href = 'login.html';
            return false;
        }
    }
    
    return true;
}

// 退出登录
function logout() {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('loginTime');
    window.location.href = 'login.html';
}

// 页面加载时自动检查登录状态
document.addEventListener('DOMContentLoaded', function() {
    // 如果当前页面不是登录页面，则检查登录状态
    if (!window.location.pathname.includes('login.html') && 
        !window.location.pathname.includes('generate_codes.html')) {
        checkAuth();
    }
});
