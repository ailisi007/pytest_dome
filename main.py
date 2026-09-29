import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RESULTS = BASE_DIR / "reports" / "allure-results"
REPORT_DIR = BASE_DIR / "reports" / "allure-report"

# ⚠️ 改成你实际安装的 Allure 路径（你环境变量配的是这个）
ALLURE_PATH = r"D:\Allure\allure-2.46.1\bin\allure.bat"

def main():
    # 确保目录存在
    RESULTS.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print("正在执行测试...")
    # pytest.ini 已经配置了 --alluredir，这里直接跑 pytest 就行
    subprocess.run([sys.executable, "-m", "pytest"], cwd=BASE_DIR)

    print("正在生成报告...")
    subprocess.run(f'"{ALLURE_PATH}" generate "{RESULTS}" -o "{REPORT_DIR}" --clean', cwd=BASE_DIR, shell=True)

    print("正在打开报告...")
    subprocess.run(f'"{ALLURE_PATH}" open "{REPORT_DIR}"', cwd=BASE_DIR, shell=True)

if __name__ == "__main__":
    main()