from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from ..models.knowledge import Knowledge
import re


class KnowledgeService:
    """知识库服务类
    
    负责管理春节相关知识库的查询、搜索和管理功能。
    包括关键词提取、相似度计算、知识检索等核心功能。
    """
    
    def __init__(self, db: Session):
        """初始化知识库服务
        
        Args:
            db: SQLAlchemy 数据库会话
        """
        self.db = db
    
    def search_knowledge(
        self,
        query: str,
        category: Optional[str] = None,
        limit: int = 5
    ) -> List[Knowledge]:
        """搜索知识库
        
        根据查询词在知识库中搜索相关内容，支持按分类筛选。
        使用关键词匹配的方式进行模糊搜索。
        
        Args:
            query: 查询词或问题
            category: 可选的分类筛选条件
            limit: 返回结果的最大数量
        
        Returns:
            List[Knowledge]: 匹配的知识列表
        """
        query_clean = self._clean_query(query)
        keywords = self._extract_keywords(query_clean)
        
        q = self.db.query(Knowledge)
        
        if category:
            q = q.filter(Knowledge.category == category)
        
        conditions = []
        for keyword in keywords:
            conditions.append(Knowledge.keywords.like(f"%{keyword}%"))
            conditions.append(Knowledge.question.like(f"%{keyword}%"))
        
        if conditions:
            q = q.filter(or_(*conditions))
        
        return q.order_by(Knowledge.priority.desc(), Knowledge.id.desc()).limit(limit).all()
    
    def get_best_match(self, query: str) -> Optional[Knowledge]:
        """获取最佳匹配的知识条目
        
        返回与查询最相关的一条知识。
        
        Args:
            query: 查询词或问题
        
        Returns:
            Optional[Knowledge]: 最佳匹配的知识，无匹配时返回 None
        """
        results = self.search_knowledge(query, limit=1)
        return results[0] if results else None
    
    def get_category_knowledge(self, category: str) -> List[Knowledge]:
        """获取指定分类的所有知识
        
        返回指定分类下的所有知识条目，按优先级排序。
        
        Args:
            category: 知识分类名称
        
        Returns:
            List[Knowledge]: 该分类下的知识列表
        """
        return self.db.query(Knowledge).filter(
            Knowledge.category == category
        ).order_by(Knowledge.priority.desc()).all()
    
    def _clean_query(self, query: str) -> str:
        """清理查询字符串
        
        去除查询字符串中的标点符号，将其替换为空格。
        
        Args:
            query: 原始查询字符串
        
        Returns:
            str: 清理后的查询字符串
        """
        query = query.strip()
        query = re.sub(r'[？?！!。.，,、;；]', ' ', query)
        return query
    
    def _extract_keywords(self, query: str) -> List[str]:
        """提取关键词
        
        从查询字符串中提取有意义的关键词，过滤停用词。
        
        Args:
            query: 清理后的查询字符串
        
        Returns:
            List[str]: 提取的关键词列表（去重）
        """
        stop_words = {'的', '了', '是', '在', '我', '你', '他', '她', '它', '们', '吗', '呢', '吧', '啊', '呀', '哦', '什么', '怎么', '如何', '哪些', '哪个', '哪个', '这个', '那个', '这些', '那些'}
        
        keywords = []
        words = query.split()
        
        for word in words:
            if len(word) >= 2 and word not in stop_words:
                keywords.append(word)
        
        return list(set(keywords))
    
    def calculate_similarity(self, query: str, knowledge: Knowledge) -> float:
        """计算查询与知识条目的相似度
        
        使用关键词重合度计算相似度分数。
        
        Args:
            query: 查询字符串
            knowledge: 知识条目对象
        
        Returns:
            float: 相似度分数（0.0-1.0）
        """
        query_clean = self._clean_query(query)
        query_keywords = set(self._extract_keywords(query_clean))
        
        knowledge_keywords = set(knowledge.keywords.split(','))
        question_keywords = set(self._extract_keywords(knowledge.question))
        
        all_keywords = knowledge_keywords | question_keywords
        
        if not query_keywords or not all_keywords:
            return 0.0
        
        intersection = query_keywords & all_keywords
        similarity = len(intersection) / len(query_keywords)
        
        return similarity
    
    def search_with_similarity(
        self,
        query: str,
        category: Optional[str] = None,
        threshold: float = 0.3
    ) -> List[Tuple[Knowledge, float]]:
        """带相似度阈值的知识搜索
        
        搜索知识并计算相似度，只返回相似度超过阈值的结果。
        
        Args:
            query: 查询字符串
            category: 可选的分类筛选
            threshold: 相似度阈值（0.0-1.0）
        
        Returns:
            List[Tuple[Knowledge, float]]: (知识条目, 相似度分数) 的列表
        """
        candidates = self.search_knowledge(query, category, limit=20)
        
        results = []
        for candidate in candidates:
            similarity = self.calculate_similarity(query, candidate)
            if similarity >= threshold:
                results.append((candidate, similarity))
        
        results.sort(key=lambda x: (-x[1], -x[0].priority))
        return results[:5]
    
    def add_knowledge(
        self,
        category: str,
        keywords: str,
        question: str,
        answer: str,
        priority: int = 0
    ) -> Knowledge:
        """添加知识条目到数据库
        
        创建新的知识条目并保存到数据库。
        
        Args:
            category: 知识分类
            keywords: 关键词（逗号分隔）
            question: 问题
            answer: 答案
            priority: 优先级（数值越大越优先）
        
        Returns:
            Knowledge: 创建的知识条目对象
        """
        knowledge = Knowledge(
            category=category,
            keywords=keywords,
            question=question,
            answer=answer,
            priority=priority
        )
        self.db.add(knowledge)
        self.db.commit()
        self.db.refresh(knowledge)
        return knowledge
    
    def batch_add_knowledge(self, knowledge_list: List[dict]) -> int:
        """批量添加知识条目
        
        一次性添加多条知识到数据库。
        
        Args:
            knowledge_list: 知识条目字典列表
        
        Returns:
            int: 成功添加的知识条目数量
        """
        count = 0
        for item in knowledge_list:
            try:
                self.add_knowledge(
                    category=item['category'],
                    keywords=item['keywords'],
                    question=item['question'],
                    answer=item['answer'],
                    priority=item.get('priority', 0)
                )
                count += 1
            except Exception as e:
                print(f"添加知识库失败: {e}")
        return count


def get_knowledge_service(db: Session) -> KnowledgeService:
    """获取知识库服务实例
    
    Args:
        db: 数据库会话
    
    Returns:
        KnowledgeService: 知识库服务实例
    """
    return KnowledgeService(db)


def init_default_knowledge(db: Session) -> int:
    knowledge_data = [
        {
            "category": "greeting",
            "keywords": "拜年,祝福,问候,新年,春节",
            "question": "如何生成拜年祝福",
            "answer": "我可以帮您生成各种拜年祝福文案！请告诉我：\n\n1. 祝福对象（长辈、领导、朋友、同事等）\n2. 希望的风格（正式、温馨、幽默等）\n3. 需要的格式（短句、长文、对联等）\n\n这样我就能为您生成合适的拜年文案了。",
            "priority": 10
        },
        {
            "category": "custom",
            "keywords": "习俗,传统,年俗,春节习俗",
            "question": "春节有哪些习俗",
            "answer": "春节有很多传统习俗，主要包括：\n\n【除夕】\n- 团圆饭：全家人一起吃年夜饭\n- 守岁：熬夜迎接新年\n- 贴春联：辞旧迎新\n- 放鞭炮：驱邪避灾\n\n【初一至初七】\n- 初一：拜年、发红包\n- 初二：回娘家\n- 初三：赤狗日（忌拜年）\n- 初四：迎灶神\n- 初五：破五（吃饺子）\n- 初六：送穷\n- 初七：人日\n\n【其他习俗】\n- 扫尘：腊月二十四\n- 祭灶：腊月二十三\n- 贴窗花、挂灯笼\n- 包饺子、做年糕\n\n南北方习俗略有不同，具体可以详细询问某个习俗。",
            "priority": 10
        },
        {
            "category": "custom",
            "keywords": "除夕,大年三十",
            "question": "除夕有什么习俗",
            "answer": "除夕（大年三十）是春节最重要的日子，习俗包括：\n\n【核心习俗】\n1. 年夜饭：全家人团聚，象征团圆\n2. 守岁：熬夜迎接新年，象征长命百岁\n3. 贴春联：辞旧迎新，祈福纳祥\n4. 放鞭炮：驱邪避灾，迎春接福\n5. 发红包：长辈给晚辈压岁钱\n\n【美食习俗】\n- 北方：饺子（象征元宝、团圆）\n- 南方：年糕（年年高升）、鱼（年年有余）\n\n【禁忌】\n- 不扫地、不倒垃圾（不扫走财气）\n- 不打骂孩子（避免新的一年不吉利）\n- 不打破碗碟（避免破财）\n\n如需了解具体某个习俗的详情，请告诉我。",
            "priority": 9
        },
        {
            "category": "custom",
            "keywords": "扫尘,大扫除,腊月二十四",
            "question": "扫尘是什么",
            "answer": "扫尘，又称大扫除、扫房子，是春节前的重要习俗。\n\n【时间】\n通常在腊月二十四进行，有\"二十四，扫房子\"的民谚。\n\n【寓意】\n- \"尘\"与\"陈\"谐音，扫尘即\"除陈布新\"\n- 清除家中的晦气和霉运\n- 迎接新年的好运和福气\n\n【做法】\n- 彻底打扫房屋卫生\n- 清洗被褥、窗帘\n- 擦拭门窗、家具\n- 重新布置家居\n\n【注意事项】\n- 从里向外扫，不把好运扫出门\n- 扫尘后可以贴春联、挂灯笼\n- 南北方具体时间略有不同\n\n扫尘象征着辞旧迎新，为新年创造整洁温馨的环境。",
            "priority": 8
        },
        {
            "category": "custom",
            "keywords": "祭灶,小年,灶王爷,腊月二十三",
            "question": "祭灶是什么",
            "answer": "祭灶，又称小年，是春节前的重要传统节日。\n\n【时间】\n- 北方：腊月二十三\n- 南方：腊月二十四\n\n【由来】\n传说灶王爷是玉皇大帝派驻人间的监察官，每年腊月二十三上天汇报一家人的善恶。\n\n【习俗】\n1. 祭灶神：供奉糖瓜、糕点\n2. 送灶神：焚烧灶神像\n3. 扫尘：开始大扫除\n\n【寓意】\n- 糖瓜：用甜食封住灶王爷的嘴，上天只说好话\n- \"上天言好事，下界保平安\"\n- 迎接新年，祈求平安\n\n【民谚】\n\"二十三，糖瓜粘；二十四，扫房子；二十五，磨豆腐；二十六，炖羊肉；二十七，宰公鸡；二十八，把面发；二十九，蒸馒头；三十晚上闹一宿，大年初一扭一扭。\"\n\n祭灶标志着春节序幕的正式拉开。",
            "priority": 8
        },
        {
            "category": "etiquette",
            "keywords": "拜年,礼仪,走亲戚",
            "question": "拜年有什么礼仪",
            "answer": "拜年礼仪是春节文化的重要组成部分，以下是一些重要礼仪：\n\n【拜年顺序】\n1. 初一：给家里长辈拜年\n2. 初二：回娘家拜年\n3. 初三以后：走亲访友\n\n【见面礼仪】\n- 见面先问好：\"新年好！\"\n- 长辈坐晚辈站\n- 双手拱手作揖或握手\n- 问候要真诚热情\n\n【红包礼仪】\n- 长辈给晚辈：压岁钱\n- 晚辈接红包：双手接过，说谢谢\n- 红包金额：讲究吉利数字\n\n【敬酒礼仪】\n- 敬酒时起身，双手持杯\n- 杯子低于长辈\n- 说话要得体礼貌\n- 适量饮酒，不劝酒\n\n【注意事项】\n- 着装整洁得体\n- 带上适当礼品\n- 注意言谈举止\n- 尊重当地习俗\n\n如需了解某个具体场景的礼仪，请告诉我。",
            "priority": 10
        },
        {
            "category": "etiquette",
            "keywords": "长辈,老人,敬酒",
            "question": "如何给长辈拜年",
            "answer": "给长辈拜年是春节的重要习俗，以下是一些要点：\n\n【拜年话术】\n- 基本问候：\"新年好！祝您身体健康！\"\n- 通用祝福：\"祝您福如东海，寿比南山！\"\n- 个性化：结合长辈情况，如\"祝您孙辈学业有成\"\n\n【拜年礼仪】\n1. 见面先问好，称呼要准确\n2. 双手拱手作揖或握手\n3. 站姿端正，面带微笑\n4. 说话要真诚温暖\n\n【注意事项】\n- 着装要整洁大方\n- 避免过于随意\n- 话语要得体温馨\n- 可以准备小礼品\n- 注意长辈的身体状况\n\n【话术示例】\n- \"爷爷，新年好！祝您身体健康，万事如意！\"\n- \"奶奶，给您拜年了！祝您福寿安康，笑口常开！\"\n- \"叔叔阿姨，新年好！祝您工作顺利，家庭幸福！\"\n\n尊重长辈是中华民族的传统美德，拜年时要格外用心。",
            "priority": 9
        },
        {
            "category": "etiquette",
            "keywords": "领导,老板,客户,商务",
            "question": "如何给领导拜年",
            "answer": "给领导拜年需要特别注意得体和分寸，以下是一些建议：\n\n【时间选择】\n- 初一至初三比较合适\n- 避免过早打扰休息\n- 提前询问是否方便\n\n【拜年方式】\n- 微信/电话：简短真诚\n- 上门拜访：准备适当礼品\n- 群发消息：不推荐\n\n【话术要点】\n1. 感谢领导的指导和帮助\n2. 表达对团队的认同\n3. 祝福领导和团队\n4. 表达对新一年的期许\n\n【话术示例】\n- \"领导，新年好！感谢您这一年的指导和帮助，祝您新年快乐，工作顺利！\"\n- \"X总，给您拜年了！感谢您的栽培，新的一年我会继续努力工作，祝您和家人身体健康！\"\n\n【注意事项】\n- 不要过于随意\n- 避免过于谄媚\n- 话语要真诚得体\n- 可以适当提到团队\n- 注意领导的时间安排\n\n商务拜年重在真诚和尊重，把握分寸很重要。",
            "priority": 9
        },
        {
            "category": "gift",
            "keywords": "送礼,礼物,年货,推荐",
            "question": "春节送什么礼物",
            "answer": "春节送礼要根据对象和关系来选择，以下是一些建议：\n\n【送给长辈】\n- 健康品：补品、保健品\n- 生活用品：保暖衣物、按摩仪\n- 传统：茶叶、酒类\n- 水果：苹果（平安）、橙子（心想事成）\n\n【送给领导】\n- 茶叶、咖啡\n- 高档酒类\n- 办公用品\n- 文化礼品\n\n【送给朋友】\n- 零食大礼包\n- 美妆护肤品\n- 数码配件\n- 创意小礼物\n\n【送给孩子】\n- 压岁钱\n- 玩具\n- 书籍\n- 学习用品\n\n【送礼原则】\n1. 适合对方\n2. 寓意吉祥\n3. 量力而行\n4. 包装精美\n5. 准备送礼物话术\n\n【禁忌】\n- 不送钟（谐音\"终\"）\n- 不送梨（谐音\"离\"）\n- 不送伞（谐音\"散\"）\n- 不送鞋（谐音\"邪\"）\n\n如需针对特定对象的建议，请告诉我。",
            "priority": 10
        },
        {
            "category": "redpacket",
            "keywords": "红包,金额,数字,吉利",
            "question": "红包金额有什么讲究",
            "answer": "红包金额有吉祥寓意的讲究，以下是一些常见的吉利数字：\n\n【经典吉利数字】\n- 6：六六大顺\n- 8：发发发\n- 9：长长久久\n- 18：要发\n- 66：六六大顺\n- 88：发发发\n- 99：长长久久\n\n【组合数字】\n- 168：一路发\n- 188：要发发\n- 288：二发发\n- 366：三六六\n- 666：六六大顺\n- 888：发发发\n- 999：长长久久\n- 1688：一路发发\n\n【按关系】\n- 长辈给晚辈：200、500、666、888\n- 平辈之间：66、88、168、188\n- 给孩子：66、88、168、288\n\n【红包留言】\n- \"新年快乐，健康成长！\"\n- \"学业进步，前程似锦！\"\n- \"马到成功，一帆风顺！\"\n- \"年年有余，万事如意！\"\n\n【注意事项】\n- 金额要适当\n- 数字要吉利\n- 留言要温馨\n- 红包要新\n\n如需针对特定关系的建议，请告诉我。",
            "priority": 10
        },
        {
            "category": "menu",
            "keywords": "年夜饭,菜单,菜谱,聚餐",
            "question": "年夜饭吃什么",
            "answer": "年夜饭是春节最重要的聚餐，以下是一些经典的菜品推荐：\n\n【北方经典】\n- 饺子：象征团圆、元宝\n- 鱼：年年有余\n- 猪蹄：挠钱\n- 年糕：年年高升\n- 四喜丸子：福禄寿喜\n\n【南方经典】\n- 年糕：年年高升\n- 鱼：年年有余\n- 鸡：大吉大利\n- 蔬菜：发财菜\n- 汤圆：团团圆圆\n\n【2026马年特色】\n- 马蹄：马到成功\n- 红烧肉：鸿运当头\n- 白菜：百财聚来\n- 豆腐：多福多寿\n\n【推荐菜单】\n【主菜】\n1. 清蒸鱼（年年有余）\n2. 红烧肉（鸿运当头）\n3. 白灼虾（哈哈大笑）\n4. 糖醋排骨（甜甜蜜蜜）\n\n【素菜】\n1. 蒜蓉西兰花（花开富贵）\n2. 白菜豆腐煲（百财多福）\n3. 荷塘小炒（和和美美）\n\n【主食】\n1. 饺子（团圆）\n2. 年糕（高升）\n\n【祝酒词】\n\"新年新气象，家家喜洋洋！祝大家身体健康，万事如意，马到成功！\"\n\n如需根据人数和口味定制菜单，请告诉我。",
            "priority": 10
        },
        {
            "category": "greeting",
            "keywords": "祝福语,文案,句子,短语",
            "question": "有哪些祝福语",
            "answer": "我可以帮您生成各种祝福语！以下是一些常见的类型：\n\n【按人群分类】\n1. 长辈：温馨、健康、吉祥\n2. 领导：正式、感恩、期许\n3. 朋友：幽默、真诚、轻松\n4. 同事：得体、协作、祝福\n5. 老师：尊敬、感恩、学业\n6. 群发：通用、简洁、大气\n\n【按风格分类】\n- 正式稳重：适合长辈、领导\n- 高情商得体：适合各种场合\n- 简短高级：红包、短句\n- 幽默搞笑：适合朋友\n- 温暖走心：适合亲密关系\n- 古风文雅：文化底蕴\n- 商务官方：职场场景\n- 可爱俏皮：年轻化\n\n【按格式分类】\n- 短句类：红包、问候\n- 长文类：私信、单独问候\n- 对联类：贴联\n- 朋友圈：图文、纯文字\n- 视频文案：短视频\n- 红包封面：2-8字\n\n请告诉我您需要哪种类型的祝福，我来帮您生成！",
            "priority": 9
        },
        {
            "category": "zodiac",
            "keywords": "马年,2026,丙午,生肖",
            "question": "2026是什么年",
            "answer": "2026年是丙午年，即马年。\n\n【基本信息】\n- 年份：2026年\n- 生肖：马\n- 天干：丙（火）\n- 地支：午（火）\n- 纳音：天河水\n\n【马年寓意】\n- 马象征：奔腾、成功、活力\n- 丙午年：火马年，热情奔放\n- 寓意：马到成功、龙马精神\n\n【马年祝福】\n\"马年大吉，马到成功！愿您如骏马奔腾，事业腾飞；似春风得意，生活幸福！\"\n\n【马年元素】\n- 马到成功\n- 龙马精神\n- 一马当先\n- 万马奔腾\n- 马年吉祥\n\n【马年禁忌】\n- 避免说\"马到成功\"的相反话\n- 尊重属马的朋友\n- 马年红色元素更旺\n\n2026马年，祝愿大家马年大吉，万事如意！",
            "priority": 10
        },
        {
            "category": "greeting",
            "keywords": "长辈,老人,父母,爷爷奶奶",
            "question": "给长辈的祝福语",
            "answer": "给长辈的祝福语要温馨、健康、吉祥，以下是一些推荐：\n\n【短句类】\n- \"新年快乐，身体健康！\"\n- \"福如东海，寿比南山！\"\n- \"年年有余，岁岁平安！\"\n- \"马年大吉，万事如意！\"\n\n【温馨类】\n\"敬爱的长辈，新年好！\n\n值此2026丙午马年新春佳节，祝您：\n身体健康，精神矍铄；\n福寿安康，笑口常开；\n龙马精神，活力不减；\n马年吉祥，万事顺遂！\n\n晚辈给您拜年了！\"\n\n【古风类】\n\"恭祝新春大吉，福寿双全！\n愿您：\n春风送暖入屠苏，\n福如东海长流水，\n寿比南山不老松。\n马年吉祥，阖家幸福！\"\n\n【正式类】\n\"尊敬的长辈：\n\n值此新春佳节，晚辈给您拜年了！\n感谢您一直以来的关爱和指导。\n新的一年，祝您：\n身体健康，心情愉悦；\n家庭和睦，幸福美满；\n马年大吉，万事如意！\"\n\n如需针对特定长辈的定制祝福，请告诉我具体情况。",
            "priority": 9
        },
        {
            "category": "greeting",
            "keywords": "领导,老板,客户,商务",
            "question": "给领导的祝福语",
            "answer": "给领导的祝福语要正式、得体、感恩，以下是一些推荐：\n\n【短句类】\n- \"新年快乐，工作顺利！\"\n- \"感谢指导，祝您事业蒸蒸日上！\"\n- \"马年大吉，再创辉煌！\"\n- \"祝您和团队新年更上一层楼！\"\n\n【正式类】\n\"尊敬的领导：\n\n新年好！\n\n感谢您这一年来对我的指导和帮助，让我在工作中收获良多。\n\n值此2026丙午马年新春，祝愿您：\n事业如骏马奔腾，蒸蒸日上；\n团队协作，再创辉煌；\n身体健康，阖家幸福；\n马年大吉，万事如意！\"\n\n【商务类】\n\"X总：\n\n给您拜年了！\n\n过去一年，感谢您的信任和支持。在您的带领下，我们团队取得了不错的成绩。\n\n新的一年，我将继续努力工作，为团队发展贡献力量。\n\n祝您：\n马到成功，事业腾飞；\n身体健康，家庭幸福；\n新年快乐，万事顺遂！\"\n\n【简洁类】\n\"领导，新年好！\n感谢您的指导，祝您2026马年事业顺利，再创辉煌！\n祝您和家人身体健康，新年快乐！\"\n\n如需针对特定领导的定制祝福，请告诉我具体情况。",
            "priority": 9
        },
        {
            "category": "schedule",
            "keywords": "安排,计划,行程,活动",
            "question": "春节怎么安排",
            "answer": "春节安排可以参考以下建议：\n\n【除夕（年三十）】\n- 下午：贴春联、包饺子\n- 晚上：年夜饭、守岁\n- 深夜：放鞭炮、迎新年\n\n【初一】\n- 上午：给长辈拜年\n- 下午：走亲访友\n- 晚上：家庭聚会\n\n【初二】\n- 全天：回娘家\n\n【初三至初五】\n- 走亲戚、访友\n- 参加聚会\n- 适当休息\n\n【初六至初七】\n- 整理家务\n- 准备开工\n- 调整作息\n\n【活动建议】\n1. 家庭聚餐\n2. 串门拜年\n3. 旅游观光\n4. 文娱活动\n5. 适当休息\n\n【注意事项】\n- 合理安排时间\n- 注意交通安全\n- 适量饮酒\n- 注意休息\n\n如需针对特定日期的详细安排，请告诉我。",
            "priority": 8
        }
    ]
    
    service = KnowledgeService(db)
    return service.batch_add_knowledge(knowledge_data)
