# Async Release Note Creation with BullMQ

Transform the synchronous release note creation into a background job system using BullMQ and Redis.

## Proposed Changes

### Backend (Garuda\backend)

#### Infrastructure
- **[MODIFY] [app.module.ts](file:///d:/Garuda/backend/src/app.module.ts)**: Configure `BullModule` to connect to Redis using credentials from `.env`.

#### CD Script Module
- **[NEW] cd-script/jobs/cd.processor.ts**: Create a BullMQ processor that:
  - Listens for `create-release-note` jobs.
  - Executes `D:\Garuda\BE_unified_state\backend\app\cd\scripts\main.py`.
  - Updates job progress and status.
- **[MODIFY] [cd-script.service.ts](file:///d:/Garuda/backend/src/cd-script/cd-script.service.ts)**: 
  - Inject the CD queue.
  - Change `executeCreateReleaseNote` to add a job to the queue and return the `jobId`.
- **[MODIFY] [cd-script.controller.ts](file:///d:/Garuda/backend/src/cd-script/cd-script.controller.ts)**: 
  - Add `GET /api/cd/jobs/:jobId` to check job status/progress.
  - Track job IDs per project (could be a simple query or stored in Redis/DB).

### Frontend (Garuda\frontend)

#### [MODIFY] [projects/[id]/release-notes/page.tsx](file:///d:/Garuda/frontend/src/app/projects/%5Bid%5D/release-notes/page.tsx)
- Update form submission to handle the `jobId` response.
- Implement a polling mechanism (e.g., `useEffect` with `setInterval`) to query the job status.
- Display UI states: `start`, `running`, `success`, `failure`, `canceled`.

## Verification Plan

### Automated Tests
- N/A (Manual verification preferred for job lifecycle).

### Manual Verification
1. Open the "Create Release Note" page for a project.
2. Submit the form.
3. Verify the UI immediately shows "Starting job..." (or similar).
4. Verify the status updates to "Running..." while the script is active.
5. Verify Success/Failure message appears based on the script result.
6. Check backend logs to confirm Redis connection and Script execution.
