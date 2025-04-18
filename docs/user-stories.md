# 🧠 User Stories

## High Priority User Stories

### US01 - Add new cards to the collection
**User Story**:  
As a user, I want to be able to add new cards to my collection, so that I can track the cards I own and their details.  
**Acceptance Criteria**:
- User can open a form to input card details (name, type, set, condition, etc.)
- Upon submitting, card is saved to their collection in the database
- Confirmation message is shown
- New card appears in the collection list

---

### US02 - Remove cards from the collection
**User Story**:  
As a user, I want to be able to remove cards from my collection, so that I can track the cards I trade or sell.  
**Acceptance Criteria**:
- Each card has a "remove" or "delete" option
- User receives a confirmation prompt before deletion
- Card is removed from the database and UI
- Confirmation message is displayed

---

### US03 - View all cards in collection  
**User Story**:  
As a user, I want to be able to view all the cards in my collection, so that I can browse what I own.  
**Acceptance Criteria**:
- Users see a grid or list view of all cards in their collection
- Card entries display name, image (if available), and key details
- Pagination or infinite scroll is available if there are many cards

---

### US04 - Edit card details  
**User Story**:  
As a user, I want to be able to edit card details (e.g., condition, set), so that my collection stays accurate.  
**Acceptance Criteria**:
- Each card has an “Edit” button
- Clicking edit opens a form with current values pre-filled
- Changes are saved to the database and UI updates in real-time
- User sees a success confirmation

---

### US05 - Manage account settings  
**User Story**:  
As a user, I want to manage my account settings, so that I can update my profile or change my password securely.  
**Acceptance Criteria**:
- User can access a "Settings" page
- User can update name, email, and password
- Form validates inputs and shows error messages if invalid
- Changes persist after saving

---

### US06 - Sort and filter cards  
**User Story**:  
As a user, I want to sort and filter cards by attributes like name, type, or rarity, so that I can easily navigate large collections.  
**Acceptance Criteria**:
- UI has dropdowns or inputs for sorting/filtering
- Sorting includes name (A-Z, Z-A), rarity, set
- Filtering includes type, colour, custom tags
- Cards update dynamically as filters are applied

---

### US07 - Tag cards with custom labels  
**User Story**:  
As a user, I want to tag my cards with custom labels, so that I can organize them into decks or categories.  
**Acceptance Criteria**:
- User can create and assign custom tags to each card
- Tags are visible on card entries
- User can filter cards by tag

---

### US08 - Search for specific cards  
**User Story**:  
As a user, I want to search for specific cards by name, so that I can quickly find what I’m looking for.  
**Acceptance Criteria**:
- Search bar is always visible or easily accessible
- Typing a name filters the list in real-time or on submit
- No results message shown if nothing matches

---

### US09 - Visualize collection statistics  
**User Story**:  
As a user, I want to see visual stats about my collection, so that I can gain insights into my card distribution.  
**Acceptance Criteria**:
- User can view charts (e.g., pie chart for rarity, bar chart for card types)
- Stats update based on the current state of the collection
- Graphs are interactive or hoverable for extra info

---

### US10 - Share cards or collection with others  
**User Story**:  
As a user, I want to share specific cards or my collection with others, so that I can collaborate or trade easily.  
**Acceptance Criteria**:
- User can select cards or collections to share
- A shareable link or user-specific access is generated
- Shared data is read-only to others
- Shared views are styled cleanly and show useful details

---

### US11 - Recommend cards that have risen the most in price  
**User Story**:  
As a user, I want to see which cards have increased the most in value, so that I can track trends and potentially sell at a good time.  
**Acceptance Criteria**:
- System fetches historical price data (via external API or uploaded data)
- A view ranks cards in the user’s collection by price change (e.g., past week/month)
- Cards with notable increases are highlighted visually
- Clicking a card provides more detailed price history

---

### US12 - Advise which cards to sell or invest in  
**User Story**:  
As a user, I want to receive suggestions about which cards might be smart to sell or invest in, so I can make informed decisions.  
**Acceptance Criteria**:
- Based on price trends, rarity, and popularity, the app highlights “Sell” or “Invest” tags
- Recommendations appear on dashboard or in a dedicated tab
- User can see reasoning for recommendation (e.g., "20% increase in 7 days", “out of print”)
- The feature clearly distinguishes between owned and unowned cards

---

### US13 - Maintain a personal wishlist of cards  
**User Story**:  
As a user, I want to maintain a wishlist of cards I want to own, so I can keep track of my collecting goals.  
**Acceptance Criteria**:
- Users can add cards to a separate “Wishlist” collection
- Wishlist shows card details and current price
- Cards can be moved from Wishlist to Collection when acquired
- User can sort, filter, or annotate Wishlist items (e.g., “high priority”)

---

## Medium Priority User Stories

### US14 - Import collection data via CSV  
**User Story**:  
As a user, I want to import my collection using a CSV file, so I can quickly get started without manually adding every card.  
**Acceptance Criteria**:
- Users can upload a `.csv` file following a specific template (e.g., card name, set, condition, quantity)
- System parses the file and adds valid entries to the collection
- Errors or duplicates are clearly reported to the user
- A template CSV file is available for download

---

### US15 - View a timeline of collection growth  
**User Story**:  
As a user, I want to see a timeline of how my collection has grown over time, so I can reflect on my progress and habits.  
**Acceptance Criteria**:
- Visual graph or timeline showing number of cards added over time
- Stats per month/quarter/year (e.g., total cards, value growth)
- Ability to filter by tags or card type in the timeline view
- Interactive elements to explore specific dates or changes

---

### US16 - Track card condition  
**User Story**:  
As a user, I want to record the condition of each card in my collection, so I can maintain accurate value estimates and manage trades.  
**Acceptance Criteria**:
- Each card entry has a field for condition (e.g., Near Mint, Lightly Played, Heavily Played)
- Condition impacts estimated value if pricing is used
- Filtering and sorting by condition is supported
- Users can update condition over time

---

### US17 - Filter and tag cards in my collection  
**User Story**:  
As a user, I want to tag my cards and filter my collection using those tags, so I can better organize by decks, sets, or trading status.  
**Acceptance Criteria**:
- Users can assign multiple custom tags to cards (e.g., “Commander”, “Foil”, “Trade”)
- A filtering UI allows users to search by one or more tags
- Tags are visible and editable from the card detail view
- Tags can be used in analytics/visualization features

---

## Low Priority User Stories

### US18 - Create and manage decks from collection  
**User Story**:  
As a user, I want to group cards from my collection into decks, so I can plan and organize actual play setups or theorycraft new builds.  
**Acceptance Criteria**:
- Users can create named decks and add/remove cards from their collection
- Decks display full card lists and quantities
- Card removal from decks does not remove them from the main collection
- Users can duplicate decks or export lists

---

### US19 - Receive alerts for price changes  
**User Story**:  
As a user, I want to get notified when cards in my collection rise or fall significantly in price, so I can make informed decisions about selling or trading.  
**Acceptance Criteria**:
- Users can opt-in to price change alerts (e.g. % increase/decrease)
- Notifications are displayed in-app or via email (if configured)
- Price data is refreshed at regular intervals from a reliable API
- Users can toggle alerts per card