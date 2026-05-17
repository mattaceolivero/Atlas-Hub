# GitHub Authorization Test Matrix

Use only owned accounts and repositories.

Synthetic marker prefix: `BB_MARKER_ATLAS_HUB_2026_05_17_`

## Accounts

| Alias | Role | GitHub username | Notes |
|---|---|---|---|
| A | Owner/Admin | mattaceolivero | Primary connected account |
| B | Collaborator/Member | acewheelie | Secondary test account |
| C | Outsider/Read-only | logged-out/incognito | No account needed for first outsider checks |

## Repositories

| Repo | Visibility | Purpose | Marker |
|---|---|---|---|
| bb-private-lab | Private | Private access baseline and collaborator removal | `BB_MARKER_ATLAS_HUB_2026_05_17_PRIVATE` |
| public-repo | Public | Public access baseline | `BB_MARKER_ATLAS_HUB_2026_05_17_PUBLIC` |
| actions-repo | Private/Public | Actions artifact/cache/log tests | `BB_MARKER_ATLAS_HUB_2026_05_17_ACTIONS` |

## Test Cases

| ID | Area | Setup | Expected | Observed | Decision |
|---|---|---|---|---|---|
| GH-AUTHZ-001 | Repo visibility transition | Private -> public -> private using owned repo | Outsider cannot access private marker after final private state |  | Pending |
| GH-AUTHZ-002 | Collaborator removal | Remove B from `bb-private-lab` | B loses web/API/git/artifact access | Baseline confirmed: `acewheelie` can see `private-marker.md` before removal | In progress |
| GH-AUTHZ-003 | GitHub App uninstall | Uninstall app from test repo | Old installation token cannot access repo after revocation window |  | Pending |
| GH-AUTHZ-004 | Actions artifact access | Generate artifact in owned repo | Only authorized users can download artifact |  | Pending |
| GH-AUTHZ-005 | npm ownership transfer | Transfer owned test package | Old owner loses publish/admin permissions |  | Pending |

## Evidence Fields

- Timestamp and timezone.
- Test account aliases.
- Repo/package/app names.
- Request URL/method or UI path.
- Expected permission.
- Observed permission.
- Screenshot/log artifact reference.
