// 新疆中考英语读写题核心训练 - 通用JS函数

// 加载词汇数据
async function loadVocabularyData() {
    try {
        const response = await fetch('vocabulary_data.json');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('加载数据失败:', error);
        return [];
    }
}

// 保存进度到 localStorage
function saveProgress(data) {
    localStorage.setItem('vocabulary_progress', JSON.stringify(data));
}

// 从 localStorage 加载进度
function loadProgress() {
    const progress = localStorage.getItem('vocabulary_progress');
    if (progress) {
        return JSON.parse(progress);
    }
    return null;
}

// 合并数据（JSON文件数据 + localStorage进度）
function mergeDataWithProgress(data, progress) {
    if (!progress) return data;
    
    return data.map(item => {
        const saved = progress.find(p => p.id === item.id);
        if (saved) {
            return { ...item, mastered: saved.mastered };
        }
        return item;
    });
}

// 获取未掌握的词汇
function getUnmasteredItems(data) {
    return data.filter(item => !item.mastered);
}

// 获取已掌握的词汇
function getMasteredItems(data) {
    return data.filter(item => item.mastered);
}

// 计算进度百分比
function calculateProgress(data) {
    const total = data.length;
    const mastered = getMasteredItems(data).length;
    const percentage = total > 0 ? Math.round((mastered / total) * 100) : 0;
    return { total, mastered, percentage };
}

// 格式化句子（将 ______ 替换为空白下划线）
function formatSentence(sentence) {
    return sentence.replace('______', '<span class="blank">______</span>');
}

// 生成选择题选项（1个正确答案 + 3个干扰项）
function generateOptions(correctAnswer, allData, currentId) {
    const options = [correctAnswer];
    
    // 从其他条目中随机选择3个干扰项
    const otherItems = allData.filter(item => 
        item.id !== currentId && 
        item.example && 
        item.example.answer && 
        item.example.answer !== '[待完善]'
    );
    
    const shuffled = otherItems.sort(() => Math.random() - 0.5);
    const distractors = shuffled.slice(0, 3).map(item => item.example.answer);
    
    options.push(...distractors);
    
    // 随机排序
    return options.sort(() => Math.random() - 0.5);
}

// 更新进度条
function updateProgressBar(total, mastered) {
    const percentage = total > 0 ? Math.round((mastered / total) * 100) : 0;
    const progressBar = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    
    if (progressBar) {
        progressBar.style.width = percentage + '%';
        progressBar.textContent = percentage + '%';
    }
    
    if (progressText) {
        progressText.textContent = `进度: ${mastered}/${total} (${percentage}%)`;
    }
}

// 显示通知
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        border-radius: 5px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
