import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.core.database import engine, Base
from app.models import User, Conversation, Message, Greeting, UserGreeting, Custom, Etiquette, GiftSuggestion, UsageLog, Knowledge


def init_database():
    print("正在初始化数据库...")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ 数据库表创建成功！")
        
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        session = Session()
        
        from app.models.greeting import TargetGroup, StyleType, FormatType
        
        sample_greetings = [
            {
                "content": "值此2026丙午马年新春佳节，祝您：马到成功，事业腾飞；龙马精神，身体健康；马年大吉，万事如意！",
                "target_group": TargetGroup.GENERAL,
                "style": StyleType.FORMAL,
                "format_type": FormatType.SENTENCE,
                "zodiac_year": "2026"
            },
            {
                "content": "新春快乐，马年吉祥！愿您在新的一年里，如骏马奔腾，事业蒸蒸日上；似春风得意，生活幸福美满。祝您和家人身体健康，万事顺遂！",
                "target_group": TargetGroup.ELDER,
                "style": StyleType.WARM,
                "format_type": FormatType.LONG,
                "zodiac_year": "2026"
            },
            {
                "content": "领导新年好！感谢您过去一年的指导与支持。2026马年，愿您事业如骏马奔腾，再创辉煌！",
                "target_group": TargetGroup.LEADER,
                "style": StyleType.BUSINESS,
                "format_type": FormatType.SENTENCE,
                "zodiac_year": "2026"
            },
            {
                "content": "朋友，马年快乐！新的一年，愿你马到成功，前程似锦，天天开心！",
                "target_group": TargetGroup.FRIEND,
                "style": StyleType.HUMOR,
                "format_type": FormatType.SENTENCE,
                "zodiac_year": "2026"
            }
        ]
        
        for greeting_data in sample_greetings:
            greeting = Greeting(**greeting_data)
            session.add(greeting)
        
        session.commit()
        print("✅ 示例数据插入成功！")
        
        from app.services.knowledge_service import init_default_knowledge
        knowledge_count = init_default_knowledge(session)
        print(f"✅ 知识库初始化完成，共{knowledge_count}条！")
        
        session.close()
        print("\n数据库初始化完成！")
        
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        raise


if __name__ == "__main__":
    init_database()
