---
title: "Printit"
description: "Archived cloud printing project. React, NestJS, Electron, C#, and an event-driven printing architecture."
draft: false
showtoc: false
weight: 92
---

Printit is an archived independent cloud printing project, now dormant and unmaintained. It did not acquire users.

I designed and built a workflow connecting customer and vendor applications with a stateless NestJS backend. The stack spans TypeScript, React, Electron, C#, PostgreSQL, and S3-compatible document storage.

Its desktop printing architecture uses a pure reducer, declarative commands, an executor for side effects, and IndexedDB persistence through Zustand. Read the [architecture article](/posts/how-i-designed-and-deployed-a-scalable-cost-efficient-print-service-architecture/) and [Electron state machine deep dive](/posts/how-i-architected-and-developed-a-pure-state-machine-inside-the-renderer-process-of-an-electron-application/).
