# GitHub Authorization Test Matrix

Use only owned accounts and repositories.

Synthetic marker prefix: `BB_MARKER_ATLAS_HUB_2026_05_17_`

## Accounts

| Alias | Role | GitHub username | Notes |
|---|---|---|---|
| A | Owner/Admin | mattaceolivero | Primary connected account |
| B | Collaborator/Member |  | Secondary test account needed |
| C | Outsider/Read-only |  | Secondary test account needed |

## Repositories

| Repo | Visibility | Purpose | Marker |
|---|---|---|---|
| public-repo | Public | Public access baseline | `BB_MARKER_ATLAS_HUB_2026_05_17_PUBLIC` |
| private-repo | Private | Private access baseline | `BB_MARKER_ATLAS_HUB_2026_05_17_PRIVATE` |
| actions-repo | Private/Public | Actions artifact/cache/log tests | `BB_MARKER_ATLAS_HUB_2026_05_17_ACTIONS` |

## Test Cases

| ID | Area | Setup | Expected | Observed | Decision |
|---|---|---|---|---|---|
| GH-AUTHZ-001 | Repo visibility transition | Private -> public -> private using owned repo | Outsider cannot access private marker after final private state |  |  |
| GH-AUTHZ-002 | Collaborator removal | Remove B from private repo | B loses web/API/git/artifact access |  |  |
| GH-AUTHZ-003 | GitHub App uninstall | Uninstall app from test repo | Old installation token cannot access repo after revocation window |  |  |
| GH-AUTHZ-004 | Actions artifact access | Generate artifact in owned repo | Only authorized users can download artifact |  |  |
| GH-AUTHZ-005 | npm ownership transfer | Transfer owned test package | Old owner loses publish/admin permissions |  |  |

## Evidence Fields

- Timestamp and timezone.
- Test account aliases.
- Repo/package/app names.
- Request URL/method or UI path.
- Expected permission.
- Observed permission.
- Screenshot/log artifact reference.
