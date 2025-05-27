#!/usr/bin/env python3
"""
KEEPダイアログ自動処理システム
睡眠不足解消のための24時間自動監視・クリックシステム
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

class KeepDialogAutomation:
    def __init__(self, keep_image_path, exec_image_path, log_dir="logs"):
        """
        KEEPダイアログ自動処理システム初期化
        
        Args:
            keep_image_path: Keep.pngのパス
            exec_image_path: exec.pngのパス（実行ボタン用）
            log_dir: ログディレクトリ
        """
        self.keep_image_path = Path(keep_image_path)
        self.exec_image_path = Path(exec_image_path)
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # ログ設定
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_dir / 'keep_automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # 動作フラグ
        self.running = False
        self.stats = {
            "start_time": None,
            "keep_clicks": 0,
            "exec_clicks": 0,
            "total_scans": 0
        }
        
        # 画像マッチング設定
        self.confidence_threshold = 0.8
        self.scan_interval = 2  # 2秒間隔でスキャン
        
        self.logger.info("KEEPダイアログ自動処理システム初期化完了")
        
    def load_template_image(self, image_path):
        """テンプレート画像の読み込み"""
        try:
            template = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
            if template is None:
                raise FileNotFoundError(f"画像ファイルが見つかりません: {image_path}")
            return template
        except Exception as e:
            self.logger.error(f"画像読み込みエラー: {e}")
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
    
    def click_at_position(self, x, y, button_type="KEEP"):
        """指定位置をクリック"""
        try:
            pyautogui.click(x, y)
            self.logger.info(f"{button_type}ボタンクリック実行: ({x}, {y})")
            
            if button_type == "KEEP":
                self.stats["keep_clicks"] += 1
            elif button_type == "EXEC":
                self.stats["exec_clicks"] += 1
                
            return True
        except Exception as e:
            self.logger.error(f"クリックエラー: {e}")
            return False
    
    def scan_and_process(self):
        """画面スキャンと自動処理のメインループ"""
        keep_template = self.load_template_image(self.keep_image_path)
        exec_template = self.load_template_image(self.exec_image_path)
        
        if keep_template is None or exec_template is None:
            self.logger.error("テンプレート画像の読み込みに失敗しました")
            return
        
        self.logger.info("🤖 KEEP自動処理開始 - あなたは安心して眠ってください！")
        
        while self.running:
            try:
                # 画面キャプチャ
                screen = self.capture_screen()
                if screen is None:
                    time.sleep(self.scan_interval)
                    continue
                
                self.stats["total_scans"] += 1
                
                # KEEPダイアログ検索
                keep_found, keep_x, keep_y, keep_conf = self.find_image_on_screen(keep_template, screen)
                
                if keep_found:
                    self.logger.warning(f"⚠️ KEEPダイアログ検出！ (信頼度: {keep_conf:.3f})")
                    
                    # KEEPボタンクリック
                    if self.click_at_position(keep_x, keep_y, "KEEP"):
                        self.logger.info("✅ KEEPボタン自動クリック完了")
                        
                        # 少し待ってから実行ボタンもチェック
                        time.sleep(1)
                        screen = self.capture_screen()
                        if screen is not None:
                            exec_found, exec_x, exec_y, exec_conf = self.find_image_on_screen(exec_template, screen)
                            if exec_found:
                                self.logger.info(f"🔺 実行ボタン検出！ (信頼度: {exec_conf:.3f})")
                                if self.click_at_position(exec_x, exec_y, "EXEC"):
                                    self.logger.info("✅ 実行ボタン自動クリック完了")
                
                # スキャン間隔待機
                time.sleep(self.scan_interval)
                
            except KeyboardInterrupt:
                self.logger.info("手動停止が要求されました")
                break
            except Exception as e:
                self.logger.error(f"処理エラー: {e}")
                time.sleep(self.scan_interval)
    
    def start_monitoring(self):
        """監視開始"""
        if self.running:
            self.logger.warning("既に監視中です")
            return
        
        self.running = True
        self.stats["start_time"] = datetime.now()
        
        # バックグラウンドで監視実行
        self.monitor_thread = threading.Thread(target=self.scan_and_process, daemon=True)
        self.monitor_thread.start()
        
        self.logger.info("🌙 24時間KEEP監視システム開始 - お疲れ様でした、ゆっくりお休みください")
    
    def stop_monitoring(self):
        """監視停止"""
        self.running = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=5)
        
        # 統計情報出力
        duration = datetime.now() - self.stats["start_time"] if self.stats["start_time"] else None
        self.logger.info("=" * 50)
        self.logger.info("📊 KEEP自動処理統計")
        self.logger.info(f"稼働時間: {duration}")
        self.logger.info(f"KEEPクリック回数: {self.stats['keep_clicks']}")
        self.logger.info(f"実行ボタンクリック回数: {self.stats['exec_clicks']}")
        self.logger.info(f"総スキャン回数: {self.stats['total_scans']}")
        self.logger.info("=" * 50)
    
    def get_status(self):
        """現在の状態取得"""
        return {
            "running": self.running,
            "stats": self.stats.copy(),
            "uptime": str(datetime.now() - self.stats["start_time"]) if self.stats["start_time"] else None
        }

def main():
    """メイン実行関数"""
    # パス設定
    keep_image = "image/Keep.png"
    exec_image = "image/exec.png"
    
    try:
        # 自動化システム初期化
        automation = KeepDialogAutomation(keep_image, exec_image)
        
        print("🤖 KEEPダイアログ自動処理システム")
        print("睡眠不足解消プログラム - あと3回の貴重なチャンス！")
        print("-" * 50)
        print("1. 開始 - 24時間監視開始")
        print("2. 停止 - 監視停止")
        print("3. 状態 - 現在の状態確認")
        print("q. 終了")
        print("-" * 50)
        
        while True:
            choice = input("\n選択してください (1/2/3/q): ").strip()
            
            if choice == "1":
                automation.start_monitoring()
                print("✅ 監視開始しました。安心してお休みください！")
                
            elif choice == "2":
                automation.stop_monitoring()
                print("⏹️ 監視を停止しました")
                
            elif choice == "3":
                status = automation.get_status()
                print(f"稼働状態: {'🟢 実行中' if status['running'] else '🔴 停止中'}")
                if status['uptime']:
                    print(f"稼働時間: {status['uptime']}")
                print(f"KEEPクリック: {status['stats']['keep_clicks']}回")
                print(f"実行クリック: {status['stats']['exec_clicks']}回")
                
            elif choice.lower() == "q":
                if automation.running:
                    automation.stop_monitoring()
                print("👋 システム終了。お疲れ様でした！")
                break
                
            else:
                print("❌ 無効な選択です")
    
    except Exception as e:
        print(f"❌ システムエラー: {e}")

if __name__ == "__main__":
    main()