#!/usr/bin/env python3
"""
自動起動スクリプト - デュアルエージェント監視を即座に開始
"""

from src.dual_agent_automation import DualAgentAutomation
import time

def auto_start():
    """自動起動関数"""
    print("🚀 トリプルエージェント自動処理システム自動起動")
    print("KEEP + Redmine + Continue 完全監視開始...")
    
    # システム初期化
    automation = DualAgentAutomation()
    
    # 即座に監視開始
    automation.start_monitoring()
    
    print("✅ 24時間トリプル監視開始完了！")
    print("😴 あなたは安心して眠ってください")
    print("🎯 KEEP + Redmine + Continue 全て自動処理中")
    print("🛑 停止するにはCtrl+Cを押してください")
    
    try:
        # システムを実行し続ける
        while automation.running:
            time.sleep(10)  # 10秒ごとにチェック
            
    except KeyboardInterrupt:
        print("\n⏹️ 手動停止が要求されました")
        automation.stop_monitoring()
        print("👋 システム終了")

if __name__ == "__main__":
    auto_start()
