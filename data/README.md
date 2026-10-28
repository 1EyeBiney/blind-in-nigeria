# Data directory

Every money figure shown on the site renders from the files here. Nothing is hand-typed into pages; a test fails the build if it finds a dollar or naira figure in a page that did not come through the money renderer. Update the data, rebuild, and the site is current.

Files:

- ledger.json: every transfer and purchase. One entry per movement of money, with date, amount in USD cents and naira, the exchange rate used, purpose, recipient organization, method, the goal it serves, and the receipt file it references (in receipts/) once received. Status is one of example, pending, sent, received. Only sent and received entries count as real; pending entries are plans; example entries show the shape and are never rendered as real.
- rates.json: exchange rates used, by date, with source. A ledger entry's rate must match one of these.
- goals.json: current goals and their monthly targets (for example, the third-meal goal). Progress is computed from ledger entries tagged with the goal id; it is never stored here.
- estimates.json: the estimated figures (feeding costs, the third meal, canes) and the counted figures (people, boarders, staff) the pages render, each with a source and the date it was last checked.
- receipts/: scanned receipts and acknowledgments, named by date and ledger entry id. Nothing goes here with bank account details visible; redact before adding.

Rules: amounts are recorded as sent and as received where they differ (fees shown, never hidden). Estimates are marked with a source and a checked date. No personal account details of any person, ever. Salaries and personal arrangements are not in this ledger; it records only gifts to organizations and purchases made for them.

The build copies these files, and a CSV of the ledger, into site/data/ so anyone can download them.
