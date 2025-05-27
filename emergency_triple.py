#!/usr/bin/env python3
"""
緊急起動 - Continue監視を含むトリプル自動化システム
"""

import time
import cv2
import numpy as np
import pyautogui
import logging
from pathlib import Path
from datetime import datetime

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/emergency_triple.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    logger.info("🚨 緊急トリプル監視システム起動")
    logger.info("監視対象: KEEP + Redmine + Continue")
    
    # 画像パス
    keep_path = "image/Keep.png"
    exec_path = "image/exec.png" 
    redmine_path = "image/redmine-agent.png"
    continue_path = "image/continue.png"
    
    # 統計
    stats = {"scans": 0, "clicks": 0}
    
    try:
        # テンプレート読み込み
        keep_template = cv2.imread(keep_path)
        exec_template = cv2.imread(exec_path)
        redmine_template = cv2.imread(redmine_path)
        continue_template = cv2.imread(continue_path)
        
        if any(t is None for t in [keep_template, exec_template, redmine_template, continue_template]):
            logger.error("❌ 画像ファイルが見つかりません")
            return
            
        logger.info("✅ 全画像読み込み完了")
        logger.info("🤖 24時間監視開始 - Continue対応版")
        
        while True:
            # 画面キャプチャ
            screenshot = pyautogui.screenshot()
            screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            stats["scans"] += 1
            
            # KEEP検索
            result = cv2.matchTemplate(screen, keep_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val >= 0.8:
                h, w = keep_template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                pyautogui.click(center_x, center_y)
                logger.warning(f"⚠️ KEEP検出・クリック: ({center_x}, {center_y})")
                stats["clicks"] += 1
            
            # Redmine検索
            result = cv2.matchTemplate(screen, redmine_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val >= 0.8:
                h, w = redmine_template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                pyautogui.click(center_x, center_y)
                logger.warning(f"🔺 Redmine検出・クリック: ({center_x}, {center_y})")
                stats["clicks"] += 1
            
            # Continue検索
            result = cv2.matchTemplate(screen, continue_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val >= 0.8:
                h, w = continue_template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                pyautogui.click(center_x, center_y)
                logger.warning(f"▶️ Continue検出・クリック: ({center_x}, {center_y}) - Continue to iterate対応！")
                stats["clicks"] += 1
            
            # 実行ボタン検索
            result = cv2.matchTemplate(screen, exec_template, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)
            if max_val >= 0.8:
                h, w = exec_template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                pyautogui.click(center_x, center_y)
                logger.warning(f"📋 実行ボタン検出・クリック: ({center_x}, {center_y})")
                stats["clicks"] += 1
            
            # 統計ログ
            if stats["scans"] % 100 == 0:
                logger.info(f"📊 {stats['scans']}回スキャン完了 | {stats['clicks']}回クリック実行")
            
            time.sleep(1.5)
            
    except KeyboardInterrupt:
        logger.info("⏹️ 手動停止")
        logger.info(f"📊 最終統計: {stats['scans']}スキャン | {stats['clicks']}クリック")
    except Exception as e:
        logger.error(f"❌ エラー: {e}")

if __name__ == "__main__":
    main()
