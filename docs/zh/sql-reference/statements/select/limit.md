---
machine_translated: true
machine_translated_rev: 5decc73b5dc60054f19087d3690c4eb99446a6c3
toc_title: LIMIT
---

# 限制 {#limit-clause}

`LIMIT m` 返回前 `m` 行数据。

`LIMIT n, m` 跳过 `n` 行数据，然后第 `n` 行后面的 `m` 行数据。 该 `LIMIT m OFFSET n` 语法是等效的。

`n` 和 `m` 必须是非负整数。

如果没有 [ORDER BY](../../../sql-reference/statements/select/order-by.md) 子句显式排序结果，结果的行选择可能是任意的和非确定性的。
