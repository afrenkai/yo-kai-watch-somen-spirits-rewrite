# Backend Logic Implementation TODO

## Stat Calculation System
- [ ] Implement `calculateStat()` function in backend
  - Takes: baseA, baseB, level, iv, ev, gymPoints, attitudeMod
  - Returns: calculated stat value
  - Formula: `floor((baseA + ((baseB - baseA + iv) * (level - 1) / 98) + floor(ev / 4) + gymPoints) * attitudeMod)`

- [ ] Implement `calculateAllStats()` endpoint/function
  - Input: yokai_id, level, ivs, evs, gym_points, attitude_id
  - Returns: { hp, str, spr, def, spd }
  - Apply attitude modifiers from database
  - Note: HP has no gym points

- [ ] Add calculated stats to Team API responses
  - When retrieving teams, include computed stats for each yokai
  - Cache calculations or compute on-demand

## Validation System
- [ ] Implement IV validation (0-15 range)
  - Validate on team create/update
  - Return validation errors

- [ ] Implement EV validation
  - Individual stat: 0-252 range
  - Total EVs: max 510 across all stats
  - Return specific error messages

- [ ] Implement Gym Points validation (0-100 range)
  - Validate on team create/update

- [ ] Implement Team composition validation
  - Min 1 yokai, max 6 yokai
  - No duplicate positions (0-5)
  - All position numbers valid
  - Return detailed error messages

## Search, Filter, Sort
- [ ] Add search query parameter to `/api/yokai/` endpoint
  - Search by: name, tribe, rank
  - Case-insensitive
  - Return matching results

- [ ] Add sorting to yokai list endpoint
  - Default sort: tier (OU > UU > NU > PU) then rank (S > A > B > C > D > E) then name
  - Optional sort parameters: tier, rank, name, stats

- [ ] Add filtering parameters
  - Filter by: tribe, rank, tier, element
  - Support multiple filters

- [ ] Add pagination
  - Default limit: 50 results
  - Support offset/limit or page/pageSize

## API Endpoints to Update

### `/api/yokai/`
- [ ] Add `?search=` query parameter
- [ ] Add `?sort=` query parameter (tier, rank, name, hp, str, spr, def, spd)
- [ ] Add `?tribe=`, `?rank=`, `?tier=` filter parameters
- [ ] Add `?limit=` and `?offset=` pagination

### `/api/teams/` (POST/PUT)
- [ ] Validate all IVs (0-15)
- [ ] Validate all EVs (0-252 individual, 510 total)
- [ ] Validate all gym points (0-100)
- [ ] Validate team composition (1-6 yokai, unique positions)
- [ ] Return 400 with detailed validation errors

### `/api/teams/{id}/` (GET)
- [ ] Include calculated stats for each yokai in response
- [ ] Format: `{ yokai_id, position, level, ..., calculated_stats: { hp, str, spr, def, spd } }`

### New Endpoint: `/api/teams/{id}/yokai/{position}/stats/` (GET)
- [ ] Calculate stats for specific yokai in team
- [ ] Return: { hp, str, spr, def, spd }
- [ ] Use current team yokai configuration

## Database/Models
- [ ] Ensure attitudes table has modifier columns (hp_mod, str_mod, spr_mod, def_mod, spd_mod)
- [ ] Add indexes for search performance (name, tribe, rank, tier)
- [ ] Consider caching calculated stats if performance becomes issue

## Testing
- [ ] Unit tests for stat calculation formulas
- [ ] Unit tests for all validation functions
- [ ] Integration tests for search/filter/sort
- [ ] Test edge cases (max EVs, min/max stats, boundary values)
- [ ] Test validation error messages

## Frontend Cleanup (Already Done)
- [x] Remove `calculateStat()` from frontend
- [x] Remove `calculateAllStats()` from frontend
- [x] Remove `validateStatValue()` from frontend
- [x] Remove `validateTotalEVs()` from frontend
- [x] Remove `validateTeam()` from frontend
- [x] Remove `sortYokaiByTier()` from frontend
- [x] Remove `filterYokai()` from frontend
- [x] Update teambuilder pages to use backend validation
- [x] Remove comments from API service files
