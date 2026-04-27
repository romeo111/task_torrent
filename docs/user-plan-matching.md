# User Plan Matching

## User Entry

TaskTorrent asks contributors for practical capacity inputs:

- AI tool
- Hourly limit
- Daily limit
- Weekly limit
- Preferred pace
- Topic preference

The goal is not to collect private billing data. The goal is to estimate how much structured AI work the contributor can safely run.

## Capacity Conversion

1 Drop is about 100k tokens of structured AI effort.

Capacity conversion should estimate available tokens over time and convert them into Drop capacity.

Examples:

- 20k usable tokens per day = 0.2 Drop/day.
- 100k usable tokens per week = 1 Drop/week.
- 30k usable tokens in one work session = 0.3 Drop/session.

## Pack And Chunk Recommendation

Recommendations should match the contributor's capacity to the smallest useful unit of work.

- Users with less than 0.15 Drop available should receive prep, review, or micro-verification tasks if available.
- Users with 0.15 to 0.3 Drop available should receive one Chunk.
- Users with 0.5 Drop available should receive two compatible Chunks or one larger review task.
- Users with 1 Drop available should receive a full Drop Pack only if they can complete and submit it cleanly.

## Topic Preference

If a contributor selects a topic preference, TaskTorrent should prioritize matching packs in that topic.

If the contributor has no preference, route them to the project demand queue. The demand queue should rank work by maintainer priority, review readiness, safety, and available chunk clarity.

## Fast Mode

Fast mode recommends the largest safe chunk or pack that fits the user's stated capacity. It should still avoid assigning work that cannot be reviewed.

## Gradual Mode

Gradual mode recommends smaller chunks first, usually 0.15 to 0.2 Drop. It is best for new contributors, sensitive domains, or projects with strict review rules.

## Default Mode

Default mode routes by demand queue first, then capacity fit, then topic preference. It should recommend a chunk that is likely to be completed, reviewed, and merged.
