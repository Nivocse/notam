import re
from . import regex
import sys


DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
NUM = "0123456789"

def periods(string):
  pattern = getattr(regex, "D_IZE")
  result = re.findall(pattern, string)
  return result[0][2:-2].strip() if result else ""

def message(string):
  pattern = getattr(regex, "MESSAGE")
  result = re.findall(pattern,string)
  return result[0][:-8] if result else ""
  

def MRLC(string):
  pattern = getattr(regex, "MRLC")
  result = re.findall(pattern, string)
  return ", ".join(result)

def FAAH(string):
  pattern = getattr(regex, "FAAH")
  result = re.findall(pattern, string)
  if not result:
    return ""
  text = ", ".join(result)
  if text[:3] in DAYS or text[0] in NUM:
    return f"AD OPEN {text}"
  while text[:3] not in DAYS and text[0] not in NUM:
    text = text[1:]
  return f"AD OPEN {text}"

def STAH(string):
  pattern = getattr(regex, "STAH")
  result = re.findall(pattern, string)
  if not result:
    return ""
  text = ", ".join(result)
  if text[:3] in DAYS or text[0] in NUM:
    return f"TWR OPS {text}"
  while text[:3] not in DAYS and text[0] not in NUM:
    text = text[1:]
  return f"TWR OPS {text}"
  

def FALC(string):
  pattern = getattr(regex, "FALC")
  result = re.findall(pattern, string)
  return f'AD CLSD {", ".join(result)}'

def ATCA(string):
  pattern = getattr(regex, "ATCA")
  result = re.findall(pattern, string)
  if not result:
    return ""
  text = ", ".join(result)
  if text[:3] in DAYS or text[0] in NUM:
    return f"ATS OPS {text}"
  while text[:3] not in DAYS and text[0] not in NUM:
    text = text[1:]
  return f"ATS OPS {text}"

def SPAH(string):
  pattern = getattr(regex, "SPAH")
  result = re.findall(pattern, string)
  if not result:
    return ""
  text = ", ".join(result)
  if text[:3] in DAYS or text[0] in NUM:
    return f"APP OPS {text}"
  while text[:3] not in DAYS and text[0] not in NUM:
    text = text[1:]
  return f"APP OPS {text}"

def ACAH(string):
  pattern = getattr(regex, "ACAH")
  result = re.findall(pattern, string)
  text = ", ".join(result)
  if not text:
    return ""
  if text[:3] in DAYS or text[0] in NUM:
    return f"ATS OPS {text}"
  while text[:3] not in DAYS and text[0] not in NUM:
    text = text[1:]
  return f"ATS OPS {text}"

def AECA(string):
  pattern = getattr(regex, "AECA")
  result = re.findall(pattern, string)
  if not result:
    return ""
  for text in result:
    if text[:3] in DAYS or text[0] in NUM:
      result[result.index(text)] = text
      continue
    while text[:3] not in DAYS and text[0] not in NUM:
      text = text[1:]
  return f'ATS OPS {", ".join(result)}'

def PIAU(string):
  pattern = getattr(regex, "PIAU")
  result = re.findall(pattern, string)
  return ", ".join(result)

def ICCT(string):
  pattern = getattr(regex, "ICCT")
  result = re.findall(pattern, string)
  if not result:
    return ""
  text = ", ".join(result)
  if not text.endswith("ON TEST"):
    text += " ON TEST"
  return text

def ICAS(string):
  pattern = getattr(regex, "ICAS")
  result = re.findall(pattern, string)
  if not result:
    return ""
  text = ", ".join(result)
  if all(c in NUM for c in text[-3:]):
    text = text[:-4]
  return f'{text} NOT AVBL'

def ISAS(string):
  pattern = getattr(regex, "ISAS")
  result = re.findall(pattern, string)
  if not result:
    return ""
  text = ", ".join(result)
  if all(c in NUM for c in text[-3:]):
    text = text[:-4]
  return f'{text} NOT AVBL'

def IGAS(string):
  pattern = getattr(regex, "IGAS")
  result = re.findall(pattern, string)
  if not result:
    return ""
  text = ", ".join(result)
  if all(c in NUM for c in text[-3:]):
    text = text[:-4]
  return f'{text} NOT AVBL'

def ILAS(string):
  pattern = getattr(regex, "ILAS")
  result = re.findall(pattern, string)
  if not result:
    return ""
  text = ", ".join(result)
  if all(c in NUM for c in text[-3:]):
    text = text[:-4]
  return f'{text} NOT AVBL'

def IUAS(string):
  pattern = getattr(regex, "IUAS")
  result = re.findall(pattern, string)
  if not result:
    return ""
  text = ", ".join(result)
  if all(c in NUM for c in text[-3:]):
    text = text[:-4]
  return f'{text} NOT AVBL'
  
def FIAU(string):
  return "NO DEICING"

def comment(string, qcode):
  period = periods(string)
  content = getattr(sys.modules[__name__], qcode)(string)

  if "BTN" in string and "BTN" not in period and qcode == "MRLC":
    return ""
  if qcode == "PIAU" and period and not content:
    return ""

  return f"{period} {content}" if period else f"{content}".replace("\n", "")
