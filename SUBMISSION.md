# Lab 0 submission

Fill in every line marked `ANSWER:`. Keep answers short (one to three sentences).
Push before the start of next week's session.

## Part A - accounts

- GitHub Education application submitted (yes/no): ANSWER:
- GitHub Education status today (approved / pending / rejected): ANSWER:
- Azure for Students subscription active (yes/no/pending): ANSWER:
- Azure budget alert created (yes/no, amount): ANSWER:

## Part B - imperative vs idempotent

1. What happened the second time you ran `make demo-imperative`? Why?
   ANSWER:

2. You fixed the error by hand and ran it again. What is wrong with `load-balancer.pool` now?
   ANSWER:

3. Remove `web-2` from the `VMS` list in `provision-idempotent.sh` and run it. Is `web-2` gone from the fake cloud? What does that tell you about guarded scripts?
   ANSWER:

## Part C - desired state

4. After `make demo-apply`, you edited `.fakecloud/web-1.json` by hand. What did `make demo-plan` show, and what is this situation called?
   ANSWER:

5. In one sentence: what did you change in `reconcile.py` to make deletion work?
   ANSWER:

## Part D - reflection

6. Give one real situation (from an internship, a job or a project) where a manual or scripted change caused a problem that a declarative tool would have prevented. If you have none, describe a plausible one.
   ANSWER:
