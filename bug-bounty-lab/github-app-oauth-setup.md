# GitHub App And OAuth Setup Notes

Create these only in owned accounts and repos.

## GitHub App

Suggested test app name: `bb-atlas-hub-test-app`

Homepage URL:

- `https://github.com/mattaceolivero/Atlas-Hub`

Webhook:

- Disable webhook unless you have an owned receiver endpoint.

Initial permissions:

- Repository contents: Read-only
- Repository metadata: Read-only
- Actions: No access
- Issues: No access

Test sequence:

1. Install on a single owned test repo.
2. Generate installation token.
3. Confirm token can only read allowed repo metadata/contents.
4. Change app permissions.
5. Remove repo from installation.
6. Uninstall app.
7. Confirm stale token behavior matches expected revocation/expiry boundaries.

Do not test against repositories you do not own.

## OAuth App

Suggested test app name: `bb-atlas-hub-oauth-test`

Callback URL:

- Use only an endpoint you own or a local loopback callback.

Test sequence:

1. Authorize with account A.
2. Authorize with account B.
3. Revoke app from account settings.
4. Confirm revoked tokens cannot access expected APIs.
5. Test redirect URI validation only within GitHub's documented OAuth App behavior and bounty ineligible list.

Note: GitHub lists some OAuth App redirect behavior as ineligible. Do not submit OAuth redirect findings unless there is concrete account/data impact beyond known behavior.
