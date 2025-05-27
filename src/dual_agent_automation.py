#!/usr/bin/env python3
"""
デュアルエージェント自動処理システム
KEEP + Redmine 両方の監視で完全睡眠確保
"""

import time
import cv2
import numpy as np
import pyautogui
import threading
import logging
from pathlib import Path
from datetime import datetime
import json

class DualAgentAutomation:
    def __init__(self):
        """
        デュアルエージェント自動処理システム初期化
        KEEP + Redmine の同時監視
        """        # 画像パス設定
        self.keep_image_path = Path("image/Keep.png")
        self.exec_image_path = Path("image/exec.png")
        self.redmine_image_path = Path("image/redmine-agent.png")
        self.continue_image_path = Path("image/continue.png")
        
        # ログディレクトリ
        self.log_dir = Path("logs")
        self.log_dir.mkdir(exist_ok=True)
          # ログ設定
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'dual_automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 動作フラグ
        self.running = False
        self.stats = {
            "start_time": None,
            "keep_detections": 0,
            "keep_clicks": 0,
            "exec_clicks": 0,
            "redmine_detections": 0,
            "redmine_clicks": 0,
            "continue_detections": 0,
            "continue_clicks": 0,
            "total_scans": 0
        }
        
        # 画像マッチング設定
        self.confidence_threshold = 0.8
        self.scan_interval = 1.5  # 1.5秒間隔でスキャン（高速化）
        
        self.logger.info("🤖 デュアルエージェント自動処理システム初期化完了")
        self.logger.info("📋 監視対象: KEEP + Redmine + Continue")
        
    def load_template_image(self, image_path):
        """テンプレート画像の読み込み"""
        try:
            template = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
            if template is None:
                raise FileNotFoundError(f"画像ファイルが見つかりません: {image_path}")
            self.logger.info(f"✅ 画像読み込み成功: {image_path}")
            return template
        except Exception as e:
            self.logger.error(f"❌ 画像読み込みエラー: {e}")
            return None
    
    def capture_screen(self):
        """画面キャプチャ"""
        try:
            screenshot = pyautogui.screenshot()
            return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        except Exception as e:
            self.logger.error(f"画面キャプチャエラー: {e}")
            return None
    
    def find_image_on_screen(self, template, screen_image):
        """
        画面上でテンプレート画像を検索
        
        Returns:
            tuple: (found, x, y, confidence) or (False, None, None, None)
        """
        try:
            result = cv2.matchTemplate(screen_image, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= self.confidence_threshold:
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return True, center_x, center_y, max_val
            
            return False, None, None, max_val
        except Exception as e:
            self.logger.error(f"画像マッチングエラー: {e}")
            return False, None, None, 0
    
    def click_at_position(self, x, y, agent_type="UNKNOWN"):
        """指定位置をクリック"""
        try:
            pyautogui.click(x, y)
            self.logger.info(f"🖱️ {agent_type}クリック実行: ({x}, {y})")
              # 統計更新
            if agent_type == "KEEP":
                self.stats["keep_clicks"] += 1
            elif agent_type == "EXEC":
                self.stats["exec_clicks"] += 1
            elif agent_type == "REDMINE":
                self.stats["redmine_clicks"] += 1
            elif agent_type == "CONTINUE":
                self.stats["continue_clicks"] += 1
                
            return True
        except Exception as e:
            self.logger.error(f"クリックエラー: {e}")
            return False
    
    def scan_and_process(self):
        """デュアル監視のメインループ"""        # テンプレート画像読み込み
        keep_template = self.load_template_image(self.keep_image_path)
        exec_template = self.load_template_image(self.exec_image_path)
        redmine_template = self.load_template_image(self.redmine_image_path)
        continue_template = self.load_template_image(self.continue_image_path)
        
        if keep_template is None or exec_template is None or redmine_template is None or continue_template is None:
            self.logger.error("❌ テンプレート画像の読み込みに失敗しました")
            return
          self.logger.info("🚀 デュアルエージェント監視開始")
        self.logger.info("😴 完全自動化 - あなたは安心して眠ってください！")
        self.logger.info("🎯 監視対象: KEEP + Redmine + Continue")
        
        while self.running:
            try:
                # 画面キャプチャ
                screen = self.capture_screen()
                if screen is None:
                    time.sleep(self.scan_interval)
                    continue
                
                self.stats["total_scans"] += 1
                
                # === KEEP ダイアログ監視 ===
                keep_found, keep_x, keep_y, keep_conf = self.find_image_on_screen(keep_template, screen)
                
                if keep_found:
                    self.stats["keep_detections"] += 1
                    self.logger.warning(f"⚠️ 右側RPA-Agent: KEEPダイアログ検出！ (信頼度: {keep_conf:.3f})")
                    
                    # KEEPボタンクリック
                    if self.click_at_position(keep_x, keep_y, "KEEP"):
                        self.logger.info("✅ KEEP自動処理完了")
                        
                        # 実行ボタンもチェック
                        time.sleep(0.5)
                        screen = self.capture_screen()
                        if screen is not None:
                            exec_found, exec_x, exec_y, exec_conf = self.find_image_on_screen(exec_template, screen)
                            if exec_found:
                                self.logger.info(f"🔺 実行ボタン検出！ (信頼度: {exec_conf:.3f})")
                                if self.click_at_position(exec_x, exec_y, "EXEC"):
                                    self.logger.info("✅ 実行ボタン自動クリック完了")
                  # === Redmine Agent 監視 ===
                redmine_found, redmine_x, redmine_y, redmine_conf = self.find_image_on_screen(redmine_template, screen)
                
                if redmine_found:
                    self.stats["redmine_detections"] += 1
                    self.logger.warning(f"🔺 左側Redmine-Agent: 三角マーク検出！ (信頼度: {redmine_conf:.3f})")
                    
                    # Redmine三角マークをクリック
                    if self.click_at_position(redmine_x, redmine_y, "REDMINE"):
                        self.logger.info("✅ Redmine三角マーク自動クリック完了")
                
                # === Continue ボタン監視 ===
                continue_found, continue_x, continue_y, continue_conf = self.find_image_on_screen(continue_template, screen)
                
                if continue_found:
                    self.stats["continue_detections"] += 1
                    self.logger.warning(f"▶️ Continueボタン検出！ (信頼度: {continue_conf:.3f})")
                    
                    # Continueボタンをクリック
                    if self.click_at_position(continue_x, continue_y, "CONTINUE"):
                        self.logger.info("✅ Continue自動クリック完了")
                  # 定期統計ログ（100スキャンごと）
                if self.stats["total_scans"] % 100 == 0:
                    uptime = datetime.now() - self.stats["start_time"]
                    self.logger.info(f"📊 スキャン{self.stats['total_scans']}回完了 | 稼働時間: {uptime}")
                    self.logger.info(f"   KEEP: {self.stats['keep_detections']}検出/{self.stats['keep_clicks']}クリック")
                    self.logger.info(f"   Redmine: {self.stats['redmine_detections']}検出/{self.stats['redmine_clicks']}クリック")
                    self.logger.info(f"   Continue: {self.stats['continue_detections']}検出/{self.stats['continue_clicks']}クリック")
                
                # スキャン間隔待機
                time.sleep(self.scan_interval)
                
            except KeyboardInterrupt:
                self.logger.info("手動停止が要求されました")
                break
            except Exception as e:
                self.logger.error(f"処理エラー: {e}")
                time.sleep(self.scan_interval)
    
    def start_monitoring(self):
        """デュアル監視開始"""
        if self.running:
            self.logger.warning("既に監視中です")
            return
        
        self.running = True
        self.stats["start_time"] = datetime.now()
        
        # バックグラウンドで監視実行
        self.monitor_thread = threading.Thread(target=self.scan_and_process, daemon=True)
        self.monitor_thread.start()
          self.logger.info("🌙 24時間デュアルエージェント監視開始")
        self.logger.info("💤 KEEP + Redmine + Continue 全て自動処理します")
        self.logger.info("🛌 お疲れ様でした、ゆっくりお休みください")
    
    def stop_monitoring(self):
        """監視停止"""
        self.running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=5)
        
        # 最終統計情報出力
        duration = datetime.now() - self.stats["start_time"] if self.stats["start_time"] else None
        self.logger.info("=" * 60)
        self.logger.info("📊 デュアルエージェント自動処理 最終統計")
        self.logger.info(f"⏰ 稼働時間: {duration}")
        self.logger.info(f"🔍 総スキャン回数: {self.stats['total_scans']}")        self.logger.info(f"🛡️ KEEP検出/クリック: {self.stats['keep_detections']}/{self.stats['keep_clicks']}")
        self.logger.info(f"🔺 Redmine検出/クリック: {self.stats['redmine_detections']}/{self.stats['redmine_clicks']}")
        self.logger.info(f"▶️ Continue検出/クリック: {self.stats['continue_detections']}/{self.stats['continue_clicks']}")
        self.logger.info(f"📋 実行ボタンクリック: {self.stats['exec_clicks']}")
        self.logger.info("=" * 60)
        self.logger.info("😴 お疲れ様でした！ゆっくり休めましたか？")
    
    def get_status(self):
        """現在の状態取得"""
        return {
            "running": self.running,
            "stats": self.stats.copy(),
            "uptime": str(datetime.now() - self.stats["start_time"]) if self.stats["start_time"] else None
        }

def main():
    """メイン実行関数"""
    try:
        # デュアル自動化システム初期化
        automation = DualAgentAutomation()
          print("🤖🔺▶️ トリプルエージェント自動処理システム")
        print("KEEP + Redmine + Continue 完全監視で絶対安眠")
        print("=" * 50)
        print("あなた: 右側RPA-Agent")
        print("監視対象: 左側Redmine-Agent + KEEPダイアログ + Continueボタン")
        print("=" * 50)
        print("1. 開始 - 24時間トリプル監視開始")
        print("2. 停止 - 監視停止") 
        print("3. 状態 - 現在の状態確認")
        print("q. 終了")
        print("=" * 50)
        
        while True:
            choice = input("\n選択してください (1/2/3/q): ").strip()
              if choice == "1":
                automation.start_monitoring()
                print("✅ トリプル監視開始！KEEP + Redmine + Continue 全て自動処理します！")
                
            elif choice == "2":
                automation.stop_monitoring()
                print("⏹️ 監視を停止しました")
                
            elif choice == "3":
                status = automation.get_status()
                print(f"\n📊 システム状態")
                print(f"稼働状態: {'🟢 実行中' if status['running'] else '🔴 停止中'}")
                if status['uptime']:
                    print(f"稼働時間: {status['uptime']}")
                print(f"KEEP処理: {status['stats']['keep_detections']}検出/{status['stats']['keep_clicks']}クリック")
                print(f"Redmine処理: {status['stats']['redmine_detections']}検出/{status['stats']['redmine_clicks']}クリック")
                print(f"Continue処理: {status['stats']['continue_detections']}検出/{status['stats']['continue_clicks']}クリック")
                print(f"総スキャン: {status['stats']['total_scans']}回")
                
            elif choice.lower() == "q":
                if automation.running:
                    automation.stop_monitoring()
                print("👋 トリプルシステム終了。お疲れ様でした！")
                break
                
            else:
                print("❌ 無効な選択です")
    
    except Exception as e:
        print(f"❌ システムエラー: {e}")

if __name__ == "__main__":
    main()
