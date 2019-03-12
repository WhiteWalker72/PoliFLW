from article_detection.src.detection import Detection

detection = Detection()

print(detection.is_political('De EASA'))
print(detection.is_political('De VVD'))

