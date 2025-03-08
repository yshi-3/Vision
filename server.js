const express = require('express');
const OpenAI = require('openai');
require('dotenv').config();

const app = express();
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
});

// 允许跨域请求
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    next();
});

// 解析 JSON 请求体
app.use(express.json());

// 处理 POST 请求
app.post('/generate', async (req, res) => {
    const { prompt } = req.body;

    if (!prompt) {
        return res.status(400).json({ error: 'Please provide a prompt.' });
    }

    try {
        // 调用 OpenAI 的 DALL·E API 生成图片
        const response = await openai.images.generate({
            model: 'dall-e-3', // 使用 DALL·E 3 模型
            prompt: prompt,
            n: 1, // 生成 1 张图片
            size: '1024x1024', // 图片尺寸
        });

        // 获取生成的图片 URL
        const imageUrl = response.data[0].url;

        // 返回图片 URL 给前端
        res.json({ imageUrl: imageUrl });
    } catch (error) {
        console.error('Error:', error);
        res.status(500).json({ error: 'Failed to generate image.' });
    }
});

// 启动服务器
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});