EV Charging Marketplace Project Document
________________________________________
🚀 Project Overview
We are building a peer-to-peer (P2P) marketplace that transforms privately owned EV chargers into rentable assets. The platform allows EV owners to find and book nearby chargers, while charger hosts earn passive income. The core innovation is in enabling access to non-smart (“dumb”) chargers through our smart adapter product and platform controls.
Our approach increases EV infrastructure availability without requiring new public charging stations, accelerating EV adoption.
________________________________________
📊 Business Model
1.	Commission Model:
o	We take a percentage fee from each charging session booked through the platform.
2.	Adapter Sales:
o	We sell smart adapters to charger owners with non-smart chargers or chargers without API access.
o	The adapter allows remote control and usage metering, enabling participation in the marketplace.
3.	Optional Premium Services (future):
o	Subscription tiers for hosts (analytics, feature boosts).
o	Insurance add-ons for hosts and users.
________________________________________
🔄 User Workflows
1. Charger Owner Onboarding Workflow
Goal: Enable a charger owner to list their charger on the platform.
Steps: 1. Owner visits the platform and clicks “Become a Host.” 2. Chooses charger type: - J1772 (non-Tesla standard) - NACS (Tesla standard) - Smart Charger (API compatible) - Dumb Charger (non-API) 3. Based on choice: - If smart with API: User logs into charger account to link. - If dumb or non-API: User is redirected to buy adapter. - If already owns adapter, user enters unique adapter ID. 4. Creates an account with personal and charger details. 5. Uploads charger photo and address (address not shown publicly). 6. Sets availability schedule (time slots per day/week). 7. Sets pricing (per hour, backend calculates per-minute equivalent). 8. Confirms KYC and agrees to terms. 9. Charger is now listed but only becomes bookable if: - Adapter is connected and online, or - API connection confirmed.
2. EV Driver Booking Workflow
Goal: Enable an EV driver to find, book, and pay for a charging session.
Steps: 1. User lands on the app and opens the map view. 2. Sees charger markers showing distance, price, availability (no exact address). 3. Taps a charger to view: - Connector type - Availability slots - Photos (to judge location) - Host rating (future) 4. To book: - Must create account. - Must complete KYC (license plate, name, vehicle type). 5. Once verified: - Full address of charger is revealed. 6. User selects desired time slot. 7. Pays to confirm booking (non-refundable if < 10 mins before start, 95% refund if canceled earlier). 8. Booking is confirmed, slot disappears for others.
3. Charging Session Flow
Goal: Enable controlled charging during the reserved time only.
Steps: 1. User arrives at the charger within scheduled time. 2. Opens app and chooses to “Start Session.” 3. Verifies presence: - Either scans QR code on charger, - Or enters in-app code onto device. 4. Platform activates charger (via API or our adapter). 5. Session runs only for paid duration. 6. When time is up: - Charging automatically stops. - Power cut remotely via adapter or API. 7. Host is credited for session.
4. Host Availability Management
Goal: Allow host to control availability and minimize abuse.
Rules: - Hosts can remove future availability at any time. - Hosts cannot cancel bookings less than 3 hours before start. - All changes to schedule reflect in real time.
________________________________________
🔐 Anti-Abuse & Platform Enforcement
Risk	Mitigation
Users bypass booking	Address revealed only after sign up and KYC
Overstaying or theft	Auto power cutoff after time. Optional alert features
Smart charger abuse	Monitoring and API usage logging
Revenue leakage	All payments must go through the app; adapter verifies presence
________________________________________
🌟 Go-to-Market Bootstrapping Plan (No Capital)
1.	Founding Host Program
o	First 100 hosts get 0% commission for 6 months or exclusive perks.
2.	Free Adapters in Exchange for Listings
o	Provide adapters free to early hosts committing to consistent availability.
3.	Referral and Loyalty Programs
o	Credits for referrals. Charging discounts for frequent users.
________________________________________
📊 Platform Benefits
To Charger Owners: - Monetize idle home infrastructure. - Set schedule and pricing flexibly. - Get paid instantly.
To EV Drivers: - Access affordable, nearby chargers. - Filter by plug type, time, location, price. - Book with trust and safety.
To the Ecosystem: - Expands available EV charging. - Encourages smart infrastructure adoption. - Unlocks passive income for households.
________________________________________
