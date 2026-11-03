from pathlib import Path
import zipfile
import re

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
DEST = WORK / 'draft/Notes'
with zipfile.ZipFile(WORK / 'before-enrichment.zip') as z:
    tree = z.read('Notes/ECE2050 Knowledge Tree.md').decode('utf-8-sig')
    glossary = z.read('Notes/Glossary.md').decode('utf-8-sig')
tree = tree.replace('[[Boolean Forms and Algebraic Simplification 1', '[[Boolean Forms and Algebraic Simplification')
tree = tree.replace('先读正文中的定义、核心方程和重要提示；需要验证过程时，再展开同一小节的推导、例题与图示。',
    '正文保留完整定义、适用前提、核心方程、求解步骤、误区和答题训练；详细推导、例题与图示按对应概念组织。先建立主线，再用例题验证边界条件。')

definitions = {
 '溢出': '数学结果超出当前表示范围；需区分无符号进位与有符号溢出，并遵循回绕／饱和规范',
 '浮点数': '用符号、有效数和指数表示数值；范围与精度分别由格式决定，零、次正规数与特殊码另行分类',
 'Q 格式': '本笔记采用 $a$ 包含符号位、$b$ 为小数位的补码定点约定，范围 $[-2^{a-1},2^{a-1}-2^{-b}]$；其他Q记法须另声明',
 '回绕': '固定宽运算丢弃超出位宽的部分，结果按模回绕；是否允许由规范决定，计数器常有意使用回绕',
 '尾数 / 有效数字': '浮点数的有效数部分；binary32正规数有隐含前导1、共24 bit精度，次正规数没有该隐含1',
 '偏移阶码': 'binary32正规数存储阶码 $E=e+127$，e为实际指数；E=0与255的解释需按特殊码规则处理',
 '隐含前导 1': '二进制正规数的前导1可不存储；零和次正规数不使用该规则',
 '格雷码': '相邻码字只差1 bit的非位权编码，常见为反射二进制格雷码；其循环相邻性不等同于CRC循环检错码',
 '校验位': '为满足奇偶约束而附加的一位；位置与位序由编码或协议规定',
 '同或门': r'两输入时检测相等，$Y=\overline{A\oplus B}$；多输入XOR归约的补表示偶数个1，不表示全部输入相等',
 '过渡带': '$V_{IL,max}<V_{in}<V_{IH,min}$ 的输入区间没有逻辑解释保证；噪声容限需另用输出保证与输入接受范围计算',
 '供电电压缩放': '不同工艺／接口使用不同额定供电；降低供电不能自动保证输入耐压、电平兼容或时序满足',
 '开关阈值': 'VTC上 $V_{in}=V_{out}$ 的点；不能直接代替输入保证阈值，曲线斜率也不足以单独决定噪声容限',
}
out = []
for line in glossary.splitlines():
    line = line.replace('[[Boolean Forms and Algebraic Simplification 1', '[[Boolean Forms and Algebraic Simplification')
    if line.startswith('| 负逻辑 / 气泡 |'):
        out += [
            '| 负逻辑 | Negative Logic | — | 电平到布尔值的映射为LOW→1、HIGH→0；与控制端低有效不是同一个概念 | [[Logic Gates and Boolean Functions#1 · Logic Gates · 统一的布尔模型|Logic Gates]] |',
            '| 反相气泡 | Inversion Bubble | — | 门符号边界上的圆圈表示取补；气泡推移须同时处理全部相应输入 | [[Universal Gates and Bubble Pushing#3 · Bubble Pushing · 全部气泡同步移动|Bubble Pushing]] |'
        ]
        continue
    for term, definition in definitions.items():
        if line.startswith('| ' + term + ' |'):
            # Preserve the final wikilink's display-text pipe as part of the fifth cell.
            parts = line.split('|', 5)
            parts[4] = ' ' + definition + ' '
            line = '|'.join(parts)
            break
    out.append(line)
glossary = '\n'.join(out) + '\n'
DEST.mkdir(parents=True, exist_ok=True)
(DEST / 'ECE2050 Knowledge Tree.md').write_text(tree, 'utf-8')
(DEST / 'Glossary.md').write_text(glossary, 'utf-8')
print('Knowledge tree and glossary staged; definitions agree with corrected notes.')
