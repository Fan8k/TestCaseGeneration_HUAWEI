#coding=utf-8
import  re

'''
验证barcode data 这种特殊规则 context 为空 from为 barcode:\d{6}
'''


if __name__ =="__main__":
   originals = [i for i in re.finditer("]", r"\r\nOK\r\r\n]\r\r\n  \(1)\UUT_SWT(1)\Qbarcode(1)\Pass [00:00:00.000]\r\r\n  qbarcode\Pass [barcode:023DUA0147258369]\r\r\n  \(1)\UUT_SWT(1)\Qbarcode(*)")]
   print(originals)