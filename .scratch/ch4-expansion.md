@@TARGET
Combinational Circuit
## Composition and state boundaries · 构成规则与状态边界

The composition rules establish a single-driver, acyclic Boolean network. They are sufficient conditions for the course's combinational model, not a classifier that turns every invalid connection into a valid sequential circuit. Shorted ordinary outputs can produce contention. An inverter loop can oscillate. A carefully designed bistable feedback circuit can store state. These outcomes require different physical and functional models.

Separate fan-out from multiple drivers. One output feeding three inputs is still one driver; three outputs tied together are three drivers. A deliberately managed tri-state bus needs an ownership protocol and released outputs, as explained in [[Tri-State Buffers and Bus Drivers]]. It is not justified merely by drawing one wire.

**Worked application.** 对 $n=AB,Y=n+C$，A/B/C 改变后需要门延迟才能得到稳定 Y，但不需要保存上一拍的 n。若改为 $n=AY$，A=1,C=0 时允许 Y=0 或1，说明仅凭当前输入不能唯一决定该反馈系统状态；是否真的稳定存储还要检查电路实现。

**English exam question:** Does a circuit without a clock necessarily have combinational behavior?

**Answer:** No. A latch can store a value without a clock edge, and an unstable feedback loop can oscillate. Determine whether the output is uniquely specified by current inputs under the stated model, then inspect state and feedback. Continue with [[Combinational Logic Design]] or [[Sequential Logic]] according to the required behavior.
@@TARGET
Boolean Equation
## Specification before implementation · 方程先描述需求

A Boolean equation states what the output must mean. It does not uniquely determine a gate topology. The same equation can be implemented with basic gates, NAND-only gates, a multiplexer, a decoder, or a lookup table. Keep the specification independent of the chosen implementation so there is an external reference for verification.

Declare the input meanings and polarity before writing algebra. If L=1 means “level is low”, a positive L term expresses an asserted low-level event even though the physical sensor could use a LOW voltage. An electrical LOW, a Boolean zero, and a deasserted alarm need not have the same meaning.

**Worked application.** 许可条件 E、故障 F、按钮 P：只在 E=1,F=0,P=1 时启动，故 $RUN=E\bar FP$。若故障输入针脚 FAULT_N=0 表示故障，则“无故障”为 FAULT_N=1，方程变为 $RUN=E\,FAULT\_N\,P$；不是把字母名字中的 N 当作另一次代数取反。

**English exam question:** Why should the variable order be declared for a minterm list?

**Answer:** The order defines each input's binary weight and therefore the row index. A correct truth condition can receive a different minterm number after the variables are reordered. Use [[Truth Table and Boolean Expression]], then compare implementation choices in [[Decoder]] and [[Multiplexer and Demultiplexer]].
@@TARGET
Boolean Axioms
## Duality and logical meaning · 对偶与逻辑含义

Boolean variables take values zero and one. AND and OR are logical operations, so ordinary numerical cancellation and division are generally unavailable. For example, A+A=A is valid Boolean idempotence; it does not imply A=0 by subtracting A as though the plus sign denoted real addition.

Duality exchanges AND with OR and zero with one while preserving the variables and their complements. Complementing a complete expression is a different operation: DeMorgan's law also complements the operands. Keeping these transformations separate prevents a common exam error.

**Worked application.** 恒等式 $A+0=A$ 的对偶是 $A\cdot1=A$，不是 $\bar A+1=\bar A$。后一式在 A=1 时左侧为1、右侧为0，立即失败。若对原等式两边取补，则应得 $\overline{A+0}=\bar A$，并经 DeMorgan 化为 $\bar A\cdot1=\bar A$。

**English exam question:** Can a useful Boolean rewrite be accepted because it works for one input pattern?

**Answer:** One passing row is an example, not a proof. Derive the rewrite from valid axioms and laws, or check every input combination with [[Proof by Perfect Induction]]. These identities become hardware transformations in [[Universal Gates and Bubble Pushing]].
@@TARGET
Laws and Rules of Boolean Algebra
## Choose the rule by structure · 看结构选择化简规则

Name the pattern before applying a rule. Absorption removes a more restrictive condition already covered by a broader condition: A+AB=A. The product AB cannot be true when A is false, so it adds no new ON rows. This reasoning is often clearer than treating the identity as an isolated formula to memorize.

The consensus term in AB+NOT A·C+BC is redundant for the steady-state Boolean function. Its removal does not necessarily preserve transient behavior: BC can bridge a path-delay gap during a change of A. Minimal literal count and hazard-free operation are different design objectives.

**Worked application.** 门控报警 $Y=A+AB+\bar AC$：先 absorption 得 $A+\bar AC$；再用 $X+\bar XY=X+Y$ 得 $A+C$。A=0 时两个式子都等于 C，A=1 时都为1，形成完整的两类逻辑解释。

**English exam question:** Why might a physically useful term be Boolean redundant?

**Answer:** Boolean algebra compares stable output values. A redundant term can still provide an additional physical path that suppresses a glitch while another path changes. Check [[Boolean Expression Simplification]] for equivalence and [[Propagation Delay and Logic Hazards]] for the timing requirement before choosing the final circuit.
@@TARGET
Proof by Perfect Induction
## Exhaustive proof and counterexamples · 穷举证明与反例

For n independent Boolean inputs, a complete truth table contains 2^n rows. Comparing both expressions on all rows proves equivalence over that domain. Checking only the rows where one expression is one does not establish that the other expression has no additional ON rows.

One mismatching row is enough to disprove an identity. It is useful to test all-zero, all-one, and boundary rows first, but those quick checks cannot replace the full proof when they pass. For a design with don't-cares, compare only the explicitly specified rows and state that limited domain.

**Worked application.** 声称 $AB+AC=A(B+C)$，四个变量组合类别由 A决定：A=0 时两侧0；A=1 时两侧B+C。也可列8行。声称 $A+B=AB$ 则在 A=1,B=0 得1≠0，一行反例足够否定。

**English exam question:** Can exhaustive testing of one-step state equations verify a long state sequence?

**Answer:** If every state-input pair matches the specified transition and output tables, repeated application preserves the specified behavior from a defined initial state. Initialization and unreachable-state policy still need checking. This connects the method to [[Synchronous Counter Design]], [[Sequence Detector]], and [[Testbench and Functional Verification]].
@@TARGET
DeMorgan's Theorems
## Move the outer complement carefully · 外层取补怎样分配

Apply DeMorgan's law to the operation enclosed by the outermost bar. Change AND to OR or OR to AND, and complement every operand at that level. If an operand is itself a compound expression, keep its parentheses and repeat the transformation there. This is a recursive operation, not a global exchange of every symbol at once.

For a NAND implementation, the output is the complement of a product. Its equivalent negative-OR symbol has complemented inputs. The gate body and bubbles must change together; moving only one bubble changes the function.

**Worked application.** $Y=\overline{(A+B)C}$，第一步为 $\overline{A+B}+\bar C$，第二步为 $\bar A\bar B+\bar C$。A=0,B=1,C=1 时原式0，正确式0；错误式 $\bar A+\bar B+\bar C$ 却为1。

**English exam question:** Does the dual of an expression equal its complement?

**Answer:** Generally no. Duality exchanges the operations and constants but leaves each literal unchanged. Complementation must invert the literals under DeMorgan's laws. Use [[Boolean Axioms]] for that distinction and [[Universal Gates and Bubble Pushing]] to carry the algebra into a gate diagram.
@@TARGET
Boolean Expression Simplification
## Preserve behavior, then evaluate cost · 先等价，再比较代价

Simplification must preserve every specified output row. Annotate intermediate steps with the identity used, especially when absorbing a term or removing a complement. A shorter expression that silently changes one legal input combination is an incorrect design, regardless of how many gates it saves.

Specify the cost metric. Literal count, number of gates, maximum fan-in, logic depth, and path delay are related but not identical. A two-level expression requiring an unavailable six-input gate may need decomposition and additional delay. Complement availability also changes the inverter count.

**Worked application.** $Y=AB+A\bar B+\bar AC$，前两项为 $A(B+\bar B)=A$；再 $A+\bar AC=A+C$。如果只能使用二输入 NOR，先产生 $n=\overline{A+C}$，再用 tied-input NOR 反相得到 Y，共两门。该实现没有说物理 delay 为零。

**English exam question:** What evidence should accompany a claimed minimum circuit?

**Answer:** State the permitted gates, available complements, and optimization metric, then show that the function is preserved on the required rows. A Boolean minimum alone is not a timing proof. Compare [[Combinational Logic Design]], [[Universal Gates and Bubble Pushing]], and [[Propagation Delay and Logic Hazards]].
@@TARGET
Minterm and Maxterm
## Row identities and polarity · 行编号与取补方向

A minterm is true on exactly one row; a maxterm is false on exactly one row. Their subscripts refer to the same input pattern, not to whether the overall function is one or zero there. For the same variable order, maxterm M_i is the complement of minterm m_i.

In a minterm, a row bit zero requires a complemented literal. In a maxterm, a row bit zero requires an uncomplemented literal so that this sum evaluates to zero on the selected row. The reversed rule follows directly from the desired output at that row.

**Worked application.** 变量顺序 ABC，索引5是101：$m_5=A\bar BC$；$M_5=\bar A+B+\bar C$。在101时前者1、后者0。在100时 m5=0，M5因 $\bar C=1$ 得1。补关系逐行成立。

**English exam question:** Why is a decoder useful for generating a canonical SOP?

**Answer:** An enabled active-high binary decoder generates one minterm per output line. OR the lines corresponding to the function's ON set. With active-low outputs, combine the complemented minterms using the appropriate NAND form. Continue to [[Decoder]] and [[Read-Only Memory and Programmable Logic Arrays]].
@@TARGET
Sum-of-Products Form
## Canonical SOP and hardware mapping · 标准与或式怎样落地

An SOP is an OR of product terms. A canonical SOP uses minterms containing every variable; a simplified SOP may omit variables within a term. Expanding a simplified term produces several minterms because the omitted variables can take either value.

Do not confuse Boolean addition with counting the number of active products. If AB and AC are both true, AB+AC is still one. Overlapping coverage is allowed. In a NAND–NAND realization, first produce each complemented product and then NAND those values to recover the OR of the original products.

**Worked application.** $Y=A\bar B$ 在变量域 ABC 内，C 可为0或1，所以 $Y=A\bar B(C+\bar C)=m_4+m_5$。若题目只有AB两个变量，标准式就是原来的 $A\bar B=m_2$，不能凭空引入C再沿用相同索引。

**English exam question:** What changes when complementary inputs are unavailable?

**Answer:** Every required complemented literal must be generated, usually adding an inverter or an equivalent tied-input NAND. The truth function remains the same, but the gate count and delay can change. Use [[Universal Gates and Bubble Pushing]] for implementation and [[Truth Table and Boolean Expression]] to check the declared variable domain.
@@TARGET
Product-of-Sums Form
## Canonical POS from OFF rows · 从零行建立标准或与式

A POS is an AND of sum terms. A canonical POS includes one maxterm for each row where the function is zero. Each selected maxterm forces the product to zero on its own row; on an ON row, all those maxterms are one, so their product is one.

The product does not include maxterms for ON rows. This reverses the selection rule used in canonical SOP, which collects ON minterms. SOP and POS can describe the same truth table even though they select opposite row sets.

**Worked application.** ABC 域中 $F=\Sigma m(1,3,5,7)$，输出其实等于C。OFF set为0,2,4,6，故 $F=\Pi M(0,2,4,6)$。逐个最大项的形式较长，但最简POS只有一个和项C；canonical并不等于minimum。

**English exam question:** Which universal-gate structure naturally implements POS?

**Answer:** A NOR–NOR network produces the complements of the sum terms and then complements their OR, yielding the AND of the original sums. Literal inverters may still be required. Compare [[POS Minimization with Karnaugh Map]], [[Universal Gates and Bubble Pushing]], and [[Sum-of-Products Form]] before choosing the lower-cost implementation.
@@TARGET
Truth Table and Boolean Expression
## A table as a verification contract · 真值表是验证契约

Use one declared variable order throughout the table, minterm list, Karnaugh map, decoder connections, and MUX select inputs. A truth table is not simply a presentation of a final expression; it is the independently stated contract used to judge every implementation.

For multiple outputs, each output has its own ON set and OFF set. Outputs may share intermediate product terms in a physical implementation, but that sharing must preserve each column separately. A valid code indicator is often an additional output rather than an interpretation guessed from the data bits.

**Worked application.** full adder 以ABC为输入，C表示carry-in。sum ON set为1,2,4,7；carry ON set为3,5,6,7。在111行，sum=1且carry=1，合成值 $1+2=3$；两列都为1并不冲突。

**English exam question:** Why can a priority encoder's data table be insufficient by itself?

**Answer:** Code zero may mean input zero is active or no input is active. A separate valid output distinguishes those cases when required by the interface. Read [[Encoder and Priority Encoder]] for that boundary and [[Half Adder and Full Adder]] for multi-output arithmetic verification.
@@TARGET
Karnaugh Map
## Group meaning and implementation choices · 圈组含义与实现选择

Each power-of-two group removes the variables that change within it. The surviving literals describe every covered row, including wrapped edge cells. Gray-code ordering makes neighboring cells differ in one variable; ordinary binary order does not preserve that adjacency around the map.

An essential prime implicant covers at least one ON cell that no other prime implicant covers. Include it, then cover the remaining required cells. A valid cover is not automatically a minimum cover; compare alternatives under the stated term/literal metric. Physical hazard requirements can justify a redundant consensus group.

**Worked application.** ABCD 域中ON set=0,2,8,10。这四行的B=D=0，而A/C全部组合都出现；四个角回绕成一组，得到 $F=\bar B\bar D$。对索引10=1010代入得1，对索引11=1011因D=1得0。

**English exam question:** Why cannot two diagonal cells be grouped merely because they look close?

**Answer:** A legal adjacent grouping corresponds to variation in exactly the eliminated variables over a rectangular power-of-two set. A diagonal pair usually differs in two variables and cannot remove just one literal. Apply the result to [[Combinational Logic Design]] and verify transient needs with [[Propagation Delay and Logic Hazards]].
@@TARGET
Karnaugh Map with Don't Cares
## Don't-care freedom and invalid-input policy · 自由度与非法输入策略

A don't-care states that the specification accepts either Boolean output on that input row. The implemented circuit still produces one definite steady-state result there. It does not physically output the symbol X or choose a value afresh during each use.

For BCD inputs, treating ten through fifteen as don't-cares is valid only when those codes are excluded or their outputs are unconstrained. If invalid codes must blank a display or raise an alarm, add that requirement to the table before minimizing. A state encoding also needs a deliberate recovery policy if invalid states can occur.

**Worked application.** 段a最简式在非法BCD输入1010上输出1，这在don't-care规范中允许；如果现在要求非法码全灭，则检测 $I_{bad}=A(B+C)$ 并令 $a_{safe}=\bar I_{bad}a$。在1010时Ibad=1，所以强制灭；原来的化简结果并没有“自动失效保护”。

**English exam question:** Must every don't-care cell be used in the final groups?

**Answer:** No. Use only those that improve a cover of required cells; a group covering only don't-cares creates no useful obligation. Check [[Seven-Segment Display and Code Conversion]] for the complete interface and [[State Encoding and Unused States]] for recovery behavior.
@@TARGET
POS Minimization with Karnaugh Map
## Read zero groups as maxterms · 零圈怎样读最大项

Group zeros rather than ones. A variable that stays zero in a zero group appears uncomplemented in the corresponding sum term; a variable that stays one appears complemented. This makes the entire sum zero precisely on the grouped rows. Variables that change disappear.

The resulting POS is the product of those sum terms. You may also minimize the complement as an SOP and apply DeMorgan's law, but clearly distinguish F from NOT F at every step. Forgetting the final complement swaps the ON and OFF sets.

**Worked application.** ABC域中，F仅在A=0,B=1时为0，C无关。OFF set为2,3；对应和项 $A+\bar B$。代入010/011得0，代入000得1，代入110得1。若误写 $\bar A+B$，就在原来的零组上得1。

**English exam question:** Are minimum SOP and minimum POS necessarily implemented at the same cost?

**Answer:** No. Their terms, literals, and required complements can differ, as can the available gate family. Compare both forms under the actual constraints. [[Universal Gates and Bubble Pushing]] maps POS into NOR networks; [[Propagation Delay and Logic Hazards]] adds the separate timing assessment.
