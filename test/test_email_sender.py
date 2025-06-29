import sys
from pathlib import Path
backend_path = Path(__file__).parent.parent / "backend"
print(backend_path)
sys.path.insert(0, str(backend_path))

from tools.mailer_tool import GmailSendMessage
def run_quick_test():
    """快速测试函数 - 用于手动验证"""
    print("=== 邮件发送功能快速测试 ===")
    
    # 测试输入数据
    test_cases = [
        {
            "name": "基本功能测试",
            "input": {
                "body": "这是一封测试邮件\n内容包含：\n- 功能验证\n- 格式测试\n- 编码测试（中文）",
                "subject": "邮件发送功能测试"
            }
        },
        {
            "name": "最小输入测试", 
            "input": {
                "body": "最小测试内容"
            }
        },
        {
            "name": "自定义收件人测试",
            "input": {
                "body": "发送给指定收件人的测试邮件",
                "subject": "自定义收件人测试",
                "to": "wyz931216309@163.com"  # 替换为真实邮箱地址
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"输入: {test_case['input']}")
        
        try:
            result = GmailSendMessage(test_case['input'])
            print(f"结果: {result}")
            
            if "成功" in result:
                print("✅ 测试通过")
            else:
                print("❌ 测试失败")
        except Exception as e:
            print(f"❌ 测试异常: {e}")
        
        print("-" * 50)

if __name__ == '__main__':
    run_quick_test()