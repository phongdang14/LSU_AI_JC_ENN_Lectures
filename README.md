# SO(3) Equivariant Neural Networks — a five-lecture journal-club series

Materials for the LSU AI Journal Club short course on SO(3)-equivariant neural
networks: from physical transformation laws, through irreducible representations
and Clebsch–Gordan couplings, to a working equivariant network built in NumPy.

No prior group theory is assumed. Basic linear algebra and some Python are enough.

**Materials are published week by week as the course is taught.** Solution notes
appear one week after their lecture, so the exercises are worth attempting first.

## Schedule and status

| # | Lecture | Central question | Notes | Notebook | Solutions |
|---|---------|------------------|:-----:|:--------:|:---------:|
| 1 | What Should Rotate? | How should a prediction change when the whole experiment is rotated? | ✅ | ✅ | — |
| 2 | Features Have Geometric Types | How does one rotation act on scalars, vectors and higher-ℓ features? | — | — | — |
| 3 | How Geometric Types Combine | How do two rotating quantities combine into one with a definite type? | — | — | — |
| 4 | From Couplings to a Neural Network | Which learned operations preserve the representation structure? | — | — | — |
| 5 | Build a Physical SO(3) ENN | How do we train, validate and extend the architecture? | — | — | — |

✅ published · — not yet released

## What is in each lecture folder

- `lecture_NN_notes.pdf` — the illustrated lecture note, self-contained, with
  discussion prompts and numbered questions.
- `lecture_NN_*.ipynb` — the participant notebook. Runs top to bottom from a
  fresh kernel; outputs are stored, so you can read it without running it.
- `lecture_NN_solutions.pdf` — answers to the numbered questions and reference
  values for the notebook checks. Added one week after the lecture.

`series-overview.pdf` is the front matter: the arc of the course, how each
90-minute session is structured, and what you should be able to do at the end.

## Running the notebooks

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Everything is NumPy, Matplotlib and SymPy — no deep-learning framework, and no
GPU. That is deliberate: the point is to see the machinery rather than call it.
The longest cell is the training loop in Lecture 5, about 40 seconds on a laptop.

## A note on the code

The networks here are written for legibility, not speed. Gradients are taken by
finite differences so that the equivariant layer is not hidden behind an autodiff
library, and the Clebsch–Gordan coefficients come from `sympy.physics.wigner`
rather than a hand-rolled solver. Every symmetry claim in the notes is checked
numerically in the notebooks, and several cells deliberately break the
architecture to show the checks failing.

## Licence

- **Lecture notes, solutions and figures** (`*.pdf`): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
  Reuse and adapt freely, including commercially, with attribution.
- **Code and notebooks** (`*.ipynb`, `*.py`, `*.sh`): [MIT](LICENSE).

## Citation

> P. Dang, *SO(3) Equivariant Neural Networks: A Five-Lecture Journal-Club
> Series*, LSU AI Journal Club, 2026. https://github.com/<user>/LSU_AI_JC_ENN_Lectures

## Credits

Author: Phong Dang. Prepared with AI assistance (ChatGPT and Claude), which
contributed to curriculum structure, technical exposition, code, review and
document production. Responsibility for the content rests with the author.

Corrections and questions are welcome — please open an issue.
