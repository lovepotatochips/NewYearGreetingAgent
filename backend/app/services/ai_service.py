from typing import List, Dict, Optional
import httpx
from ..core.config import settings
import json


class AIService:
    """AI 服务类
    
    负责与 OpenAI API 进行交互，生成拜年祝福文案、优化文本等功能。
    在没有配置 API 密钥时，使用模拟响应作为后备方案。
    """
    
    def __init__(self):
        """初始化 AI 服务
        
        从配置中获取 API 密钥，如果没有配置则使用模拟密钥。
        """
        self.api_key = settings.AI_API_KEY if hasattr(settings, 'AI_API_KEY') else "mock_key"
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """调用 OpenAI 聊天完成接口
        
        向 OpenAI API 发送聊天请求，获取 AI 回复。
        如果请求失败，使用模拟响应作为后备。
        
        Args:
            messages: 消息列表，格式为 [{"role": "user/assistant", "content": "..."}]
            system_prompt: 系统提示词，定义 AI 的角色和任务
            temperature: 温度参数，控制回复的随机性（0-1）
            max_tokens: 最大生成 token 数
        
        Returns:
            str: AI 生成的回复内容
        """
        if system_prompt:
            messages.insert(0, {"role": "system", "content": system_prompt})
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "gpt-3.5-turbo",
                        "messages": messages,
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                )
                response.raise_for_status()
                result = response.json()
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            return self._mock_response(messages[-1]["content"])
    
    def _mock_response(self, user_message: str) -> str:
        """生成模拟响应
        
        当 AI API 不可用时，根据用户消息内容返回预设的模拟响应。
        
        Args:
            user_message: 用户的消息内容
        
        Returns:
            str: 模拟的回复内容
        """
        message_lower = user_message.lower()
        
        if "拜年" in user_message or "祝福" in user_message:
            return "您好！我可以帮您生成各种拜年祝福文案。请告诉我：\n1. 您要祝福的对象（长辈、领导、朋友等）\n2. 希望的风格（正式、幽默、温馨等）\n3. 需要的格式（短句、长文、对联等）\n\n这样我就能为您生成合适的拜年文案了！"
        
        elif "习俗" in user_message or "传统" in user_message:
            return "关于春节习俗，我可以为您解答：\n- 除夕到初七的各种习俗\n- 南北方习俗差异\n- 祭灶、扫尘等传统流程\n- 各种习俗的寓意和禁忌\n\n请告诉我您想了解哪个方面的习俗？"
        
        elif "礼仪" in user_message:
            return "关于拜年礼仪，我可以为您提供：\n- 走亲戚的顺序\n- 面对面拜年话术\n- 敬酒礼仪\n- 红包礼仪\n- 职场拜年礼仪\n\n请告诉我您需要哪方面的礼仪指导？"
        
        else:
            return f"我理解您的问题是：{user_message}\n\n作为拜年助手，我可以帮您：\n1. 生成拜年祝福文案\n2. 优化和改写文案\n3. 解答春节习俗问题\n4. 提供礼仪指导\n5. 推荐礼物和红包\n6. 安排年夜饭\n7. 其他实用建议\n\n请告诉我您需要什么帮助？"
    
    async def generate_greeting(
        self,
        target_group: str,
        style: str,
        format_type: str,
        keywords: List[str] = None,
        count: int = 1
    ) -> List[str]:
        """生成拜年祝福文案
        
        使用 AI 生成指定数量和要求的拜年祝福文案。
        
        Args:
            target_group: 目标人群（长辈、领导、朋友等）
            style: 文案风格（正式、温馨、幽默等）
            format_type: 格式类型（短句、长文、对联等）
            keywords: 可选的关键词列表
            count: 生成的文案数量
        
        Returns:
            List[str]: 生成的祝福文案列表
        """
        prompt = f"""
        请生成{count}条拜年祝福文案，要求：
        - 目标人群：{target_group}
        - 风格：{style}
        - 格式：{format_type}
        - 生肖年：2026丙午马年
        - 关键词：{', '.join(keywords) if keywords else '无'}
        - 要求：贴合马年元素，避免土味生硬，得体大方
        """
        
        response = await self.chat_completion([{"role": "user", "content": prompt}])
        
        greetings = []
        lines = response.split('\n')
        current_greeting = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                if current_greeting:
                    greetings.append('\n'.join(current_greeting))
                current_greeting = [line[2:]]
            else:
                current_greeting.append(line)
        
        if current_greeting:
            greetings.append('\n'.join(current_greeting))
        
        return greetings[:count] if greetings else [response]
    
    async def optimize_text(
        self,
        content: str,
        target_style: str = None,
        target_group: str = None,
        length_adjust: str = None
    ) -> str:
        """优化拜年文案
        
        使用 AI 优化用户提供的拜年文案，使其更加得体、精美。
        
        Args:
            content: 原始文案内容
            target_style: 目标风格（可选）
            target_group: 目标人群（可选）
            length_adjust: 长度调整（缩短/加长/保持）
        
        Returns:
            str: 优化后的文案内容
        """
        prompt = f"""
        请优化以下拜年文案：
        
        原文：{content}
        
        优化要求：
        - 目标风格：{target_style if target_style else '保持原风格'}
        - 目标人群：{target_group if target_group else '保持原人群'}
        - 长度调整：{length_adjust if length_adjust else '保持原长度'}
        - 修正语病、优化措辞
        - 融入2026马年元素
        """
        
        return await self.chat_completion([{"role": "user", "content": prompt}])


ai_service = AIService()
