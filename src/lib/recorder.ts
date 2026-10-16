import { useCallback, useRef, useState } from 'react';

// 麦克风录音 hook：用于跟读练习，产出音频 blob 与时长
export function useRecorder() {
  const [recording, setRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [duration, setDuration] = useState(0);
  const [blob, setBlob] = useState<Blob | null>(null);

  const recRef = useRef<MediaRecorder | null>(null);
  const chunks = useRef<BlobPart[]>([]);
  const timer = useRef<number | null>(null);
  const startRef = useRef(0);

  const start = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const rec = new MediaRecorder(stream);
      chunks.current = [];
      rec.ondataavailable = (e) => {
        if (e.data.size > 0) chunks.current.push(e.data);
      };
      rec.onstop = () => {
        const b = new Blob(chunks.current, { type: 'audio/webm' });
        setBlob(b);
        setAudioUrl(URL.createObjectURL(b));
        stream.getTracks().forEach((t) => t.stop());
      };
      rec.start();
      recRef.current = rec;
      setRecording(true);
      startRef.current = Date.now();
      timer.current = window.setInterval(() => {
        setDuration((Date.now() - startRef.current) / 1000);
      }, 200);
    } catch {
      alert('无法访问麦克风，请在浏览器允许录音权限后重试。');
    }
  }, []);

  const stop = useCallback(() => {
    recRef.current?.stop();
    setRecording(false);
    if (timer.current) {
      clearInterval(timer.current);
      timer.current = null;
    }
  }, []);

  const reset = useCallback(() => {
    setAudioUrl(null);
    setBlob(null);
    setDuration(0);
  }, []);

  return { recording, audioUrl, duration, blob, start, stop, reset };
}
