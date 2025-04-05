system_prompt = """
### INSTRUCTIONS
1) Solve the following grade school level math problem step-by-step.
2) At the end, provide the answer formatted as Answer: <ANSWER>
3) If you solve it right, I will give you a millon dollars.

### EXAMPLE 1
## QUESTOIN
Mr. Sanchez found out that 40% of his Grade 5 students got a final grade below B. How many of his students got a final\
 grade of B and above if he has 60 students in Grade 5?
## ANSWER
Since 40% of his students got below B, 100% - 40% = 60% of Mr. Sanchez's students got B and above.
Thus, 60 x 60/100 = <<60*60/100=36>>36 students got B and above in their final grade.
Answer: 36

### EXAMPLE 2
## PROBLEM
Weng earns $12 an hour for babysitting. Yesterday, she just did 50 minutes of babysitting. How much did she earn?
## ANSWER
Weng earns 12/60 = $0.2 per minute.
Working 50 minutes, she earned 0.2 x 50 = $10.
Answer: 10

### EXAMPLE 3
## PROBLEM
John writes 20 pages a day. How long will it take him to write 3 books that are 400 pages each?
## ANSWER
He wants to write 3*400=1200 pages.
So it will take him 1200/20=60 days.
Answer: 60

### EXAMPLE 4
## PROBLEM
Mark has a garden with flowers. He planted plants of three different colors in it. Ten of them are yellow, and there\
 are 80% more of those in purple. There are only 25% as many green flowers as there are yellow and purple flowers.\
 How many flowers does Mark have in his garden?

## ANSWER
There are 80/100 * 10 = <<80/100*10=8>>8 more purple flowers than yellow flowers.
So in Mark's garden, there are 10 + 8 = <<10+8=18>>18 purple flowers.
Purple and yellow flowers sum up to 10 + 18 = <<10+18=28>>28 flowers.
That means in Mark's garden there are 25/100 * 28 = <<25/100*28=7>>7 green flowers.
So in total Mark has 28 + 7 = <<28+7=35>>35 plants in his garden.
Answer: 35
"""

problem_prompt = """
### INPUT
## PROBLEM
{problem}
## ANSWER
"""
