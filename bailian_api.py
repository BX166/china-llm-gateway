# -*- coding: utf-8 -*-
"""阿里百炼 DashScope 视频生成 API 封装
鉴权：Bearer Token (sk-xxx)
API基址：https://dashscope.aliyuncs.com/api/v1
文档：https://help.aliyun.com/zh/model-studio/video-generation-api/

模型：
- happyhorse-1.0-t2v：音视频联合生成（对白语音+环境音+口型同步，推荐！）
- wanx2.1-t2v-turbo：文生视频快速版（纯视频，无声）
- wanx2.1-t2v-plus：文生视频高质量版（纯视频，无声）
"""
import urllib.request
import urllib.error
import json
import time
import os

KEY = 'sk-552ee3495e6b4741b3818680dd220f75'
BASE = 'https://dashscope.aliyuncs.com/api/v1'


class BailianAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('BAILIAN_API_KEY', KEY)

    def _req(self, method, path, body=None):
        url = f'{BASE}{path}'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        if 'video-synthesis' in path:
            headers['X-DashScope-Async'] = 'enable'
        data = json.dumps(body).encode() if body else None
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            return json.loads(e.read().decode())

    def text2video(self, prompt, model='wanx2.1-t2v-turbo',
                   size='1280*720', duration=5, seed=None, negative_prompt=''):
        """文生视频（异步）
        - model: wanx2.1-t2v-turbo（快速）/ wanx2.1-t2v-plus（高质量）/ happyhorse-1.0-t2v（音视频联合）
        - size: '1280*720'（横屏16:9）/ '720*1280'（竖屏9:16）
        - duration: 视频时长（秒），5/10（wanx）/ 5-15（happyhorse）
        - seed: 随机种子（固定可复现结果）
        返回 task_id，用 query_task() 轮询
        """
        body = {
            'model': model,
            'input': {'prompt': prompt},
            'parameters': {'size': size, 'duration': duration}
        }
        if seed is not None:
            body['parameters']['seed'] = seed
        if negative_prompt:
            body['parameters']['negative_prompt'] = negative_prompt
        return self._req('POST', '/services/aigc/video-generation/video-synthesis', body)

    def text2video_r2v(self, prompt, reference_images, model='happyhorse-1.0-r2v',
                       resolution='720P', ratio='16:9', duration=5, seed=None):
        """参考图生视频（R2V，异步）
        - model: happyhorse-1.0-r2v
        - prompt: 提示词，用 [Image N] 引用参考图（N 从 1 开始）
        - reference_images: 参考图路径列表，顺序对应 [Image 1], [Image 2]...
        - resolution: '720P' 或 '1080P'
        - ratio: '16:9', '9:16', '1:1'
        - duration: 5-15 秒
        返回 task_id，用 query_task() 轮询
        """
        import base64
        media = []
        for path in reference_images:
            with open(path, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode()
            media.append({
                'type': 'reference_image',
                'url': f'data:image/png;base64,{b64}'
            })
        body = {
            'model': model,
            'input': {
                'prompt': prompt,
                'media': media
            },
            'parameters': {
                'resolution': resolution,
                'ratio': ratio,
                'duration': duration
            }
        }
        if seed is not None:
            body['parameters']['seed'] = seed
        return self._req('POST', '/services/aigc/video-generation/video-synthesis', body)

    def query_task(self, task_id):
        """查询任务状态
        返回 output.task_status: PENDING / RUNNING / SUCCEEDED / FAILED
        SUCCEEDED 时 output.video_url 包含视频地址
        """
        return self._req('GET', f'/tasks/{task_id}')

    def poll(self, task_id, interval=15, timeout=900):
        """轮询直到任务完成（视频生成通常3-10分钟）"""
        start = time.time()
        while time.time() - start < timeout:
            r = self.query_task(task_id)
            status = r.get('output', {}).get('task_status', '')
            if status == 'SUCCEEDED':
                return r
            elif status == 'FAILED':
                raise RuntimeError(f'Task failed: {r}')
            print(f'  {status}... ({int(time.time() - start)}s elapsed)')
            time.sleep(interval)
        raise TimeoutError(f'Task {task_id} timed out after {timeout}s')

    def download_video(self, url, output_path):
        """下载生成的视频"""
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=120) as resp:
            with open(output_path, 'wb') as f:
                f.write(resp.read())
        return output_path


if __name__ == '__main__':
    api = BailianAPI()
    r = api.text2video('测试视频：一只猫', model='wanx2.1-t2v-turbo', size='1280*720')
    print(json.dumps(r, ensure_ascii=False, indent=2))
