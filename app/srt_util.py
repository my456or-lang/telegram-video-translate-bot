import pysrt


def sec_to_srt_time(t: float):
hours = int(t // 3600)
minutes = int((t % 3600) // 60)
seconds = int(t % 60)
milliseconds = int((t - int(t)) * 1000)
return pysrt.SubRipTime(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)


def segments_to_srt(segments, translated_text, out_path):
subs = pysrt.SubRipFile()
subs.append(pysrt.SubRipItem(index=1, start=sec_to_srt_time(0), end=sec_to_srt_time(9999), text=translated_text))
subs.save(out_path, encoding='utf-8')
