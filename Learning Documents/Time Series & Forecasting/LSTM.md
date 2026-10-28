# LSTM Algorithm — Beginner-Friendly Guide

## 1. What is LSTM?

**LSTM** stands for **Long Short-Term Memory**.

It is a special type of **Recurrent Neural Network (RNN)** designed to learn from sequence data such as:

- Text
- Time-series data
- Speech
- Stock prices
- Sensor readings
- Weather data

A normal RNN can struggle to remember information from many steps ago.  
LSTM solves this problem by using a **memory cell** and several **gates**.

---

## 2. Why Do We Need LSTM?

Imagine this sentence:

> I grew up in France, so I speak fluent ______.

To predict the missing word **French**, the model needs to remember the word **France**, even if many words appear between them.

A simple RNN may forget older information.

An LSTM is designed to keep useful information for longer periods.

---

## 3. Main Idea

An LSTM decides:

1. What old information should be forgotten?
2. What new information should be remembered?
3. What information should be used as the output?

It does this using three main gates:

- **Forget Gate**
- **Input Gate**
- **Output Gate**

The LSTM also has a **Cell State**, which acts like long-term memory.

---

## 4. Important Variables

At time step `t`:

| Symbol | Meaning |
|---|---|
| `x_t` | Current input |
| `h_(t-1)` | Previous hidden state |
| `C_(t-1)` | Previous cell state |
| `h_t` | New hidden state |
| `C_t` | New cell state |

You can think of:

- **Cell state `C_t`** = long-term memory
- **Hidden state `h_t`** = current working memory / output

---

# 5. LSTM Step-by-Step

## Step 1: Forget Gate

The forget gate decides what information should be removed from the previous cell state.

### Formula

```text
f_t = sigmoid(W_f · [h_(t-1), x_t] + b_f)
```

The sigmoid function gives values between `0` and `1`.

- `0` means: forget this information
- `1` means: keep this information

### Simple Example

Suppose the LSTM was processing:

> John lives in London.

Later the text says:

> John moved to Paris.

The model may need to forget **London** and remember **Paris**.

---

## Step 2: Input Gate

The input gate decides what new information should be stored.

### Input gate

```text
i_t = sigmoid(W_i · [h_(t-1), x_t] + b_i)
```

### Candidate memory

```text
C~_t = tanh(W_C · [h_(t-1), x_t] + b_C)
```

The candidate memory contains possible new information.

---

## Step 3: Update the Cell State

Now the LSTM combines:

- Old memory that should be kept
- New information that should be added

### Formula

```text
C_t = f_t * C_(t-1) + i_t * C~_t
```

This is the main memory update step.

---

## Step 4: Output Gate

The output gate decides what part of the cell state should become the hidden state.

### Formula

```text
o_t = sigmoid(W_o · [h_(t-1), x_t] + b_o)
```

Then:

```text
h_t = o_t * tanh(C_t)
```

The new hidden state `h_t` can be:

- Sent to the next time step
- Used for prediction

---

# 6. Complete LSTM Algorithm

For every input `x_t` in the sequence:

```text
1. Calculate forget gate:
   f_t = sigmoid(W_f · [h_(t-1), x_t] + b_f)

2. Calculate input gate:
   i_t = sigmoid(W_i · [h_(t-1), x_t] + b_i)

3. Calculate candidate memory:
   C~_t = tanh(W_C · [h_(t-1), x_t] + b_C)

4. Update cell state:
   C_t = f_t * C_(t-1) + i_t * C~_t

5. Calculate output gate:
   o_t = sigmoid(W_o · [h_(t-1), x_t] + b_o)

6. Calculate hidden state:
   h_t = o_t * tanh(C_t)

7. Pass h_t and C_t to the next time step.
```

---

# 7. Easy Visual Flow

```text
Previous Hidden State h_(t-1)
            |
            v
Current Input x_t
            |
            v
    +----------------+
    |   Forget Gate  |
    +----------------+
            |
            v
Decide what old memory to keep
            |
            v
    +----------------+
    |   Input Gate   |
    +----------------+
            |
            v
Decide what new information to store
            |
            v
    +----------------+
    |   Cell State   |
    +----------------+
            |
            v
Update long-term memory
            |
            v
    +----------------+
    |  Output Gate   |
    +----------------+
            |
            v
New Hidden State h_t
```

---

# 8. What Are Sigmoid and Tanh?

## Sigmoid

The sigmoid function returns a value between `0` and `1`.

```text
sigmoid(x) = 1 / (1 + e^(-x))
```

It is useful for gates because it behaves like a percentage.

Example:

```text
0.0 -> keep almost nothing
0.5 -> keep about half
1.0 -> keep almost everything
```

---

## Tanh

The `tanh` function returns values between `-1` and `1`.

It is commonly used to create and transform memory values.

---

# 9. Simple Pseudocode

```text
initialize hidden_state = 0
initialize cell_state = 0

for each input in sequence:

    forget = sigmoid(input + hidden_state)

    input_gate = sigmoid(input + hidden_state)

    candidate_memory = tanh(input + hidden_state)

    cell_state =
        forget * cell_state
        + input_gate * candidate_memory

    output_gate = sigmoid(input + hidden_state)

    hidden_state =
        output_gate * tanh(cell_state)

return hidden_state
```

This pseudocode is simplified.  
Real LSTM networks use learned weight matrices and bias values.

---

# 10. Simple LSTM Example in Python

Using TensorFlow / Keras:

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

model = Sequential()

model.add(
    LSTM(
        units=64,
        input_shape=(10, 1)
    )
)

model.add(Dense(1))

model.compile(
    optimizer="adam",
    loss="mse"
)

model.summary()
```

### Meaning

```text
units=64
```

means the LSTM has 64 hidden units.

```text
input_shape=(10, 1)
```

means:

- 10 time steps
- 1 feature at each time step

---

# 11. Example Input Shape

Suppose we have temperature data:

```text
Day 1 -> 30°C
Day 2 -> 31°C
Day 3 -> 29°C
Day 4 -> 32°C
Day 5 -> 33°C
```

We could use previous temperatures to predict the next temperature.

Example training input:

```text
[30, 31, 29, 32]
```

Target:

```text
33
```

The LSTM tries to learn patterns in the sequence.

---

# 12. LSTM vs Normal RNN

| Feature | RNN | LSTM |
|---|---|---|
| Handles sequences | Yes | Yes |
| Remembers long-term information | Weak | Better |
| Has gates | No | Yes |
| Has cell state | No | Yes |
| Vanishing-gradient problem | Common | Reduced |
| Complexity | Lower | Higher |

---

# 13. LSTM vs GRU

A **GRU** is another gated recurrent network.

| Feature | LSTM | GRU |
|---|---|---|
| Main gates | 3 | 2 |
| Cell state | Separate | Combined |
| Parameters | More | Fewer |
| Training speed | Usually slower | Usually faster |
| Long-sequence modeling | Strong | Strong |

There is no rule that one is always better.  
The best choice depends on the dataset and problem.

---

# 14. Common Applications of LSTM

LSTMs can be used for:

### Text

- Sentiment analysis
- Text classification
- Language modeling
- Named-entity recognition

### Time Series

- Sales prediction
- Energy demand forecasting
- Weather prediction
- Sensor forecasting

### Audio

- Speech recognition
- Sound classification

### Other Sequence Problems

- Activity recognition
- Anomaly detection
- Machine monitoring

---

# 15. Training an LSTM

Training usually follows these steps:

```text
1. Prepare sequence data
2. Normalize or encode the data
3. Split into training and testing sets
4. Create sequences
5. Build the LSTM model
6. Choose a loss function
7. Choose an optimizer
8. Train the model
9. Evaluate the model
10. Make predictions
```

The network learns its weights using **Backpropagation Through Time (BPTT)**.

---

# 16. Key Idea to Remember

An LSTM can be understood as a memory system with three questions:

```text
Forget Gate:
"What should I forget?"

Input Gate:
"What should I learn?"

Output Gate:
"What should I output?"
```

And the **cell state** is the model's longer-term memory.

---

# 17. Short Summary

```text
Input x_t
   |
   v
Forget Gate
   |
   v
Remove unnecessary old information
   |
   v
Input Gate
   |
   v
Add useful new information
   |
   v
Update Cell State
   |
   v
Output Gate
   |
   v
Generate Hidden State / Prediction
```

The core equations are:

```text
f_t = sigmoid(W_f [h_(t-1), x_t] + b_f)

i_t = sigmoid(W_i [h_(t-1), x_t] + b_i)

C~_t = tanh(W_C [h_(t-1), x_t] + b_C)

C_t = f_t * C_(t-1) + i_t * C~_t

o_t = sigmoid(W_o [h_(t-1), x_t] + b_o)

h_t = o_t * tanh(C_t)
```

---

# 18. One-Line Definition

> **LSTM is a type of recurrent neural network that uses gates and a memory cell to decide what information to forget, remember, and output over a sequence.**

---

## Beginner Tip

Do not try to memorize all equations immediately.

First remember this idea:

```text
FORGET old information
     +
LEARN new information
     +
UPDATE memory
     +
OUTPUT useful information
```

Once this flow is clear, the equations become much easier to understand.
