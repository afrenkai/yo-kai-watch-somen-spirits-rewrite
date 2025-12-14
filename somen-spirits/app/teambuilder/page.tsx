'use client';

import { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Image from 'next/image';
import styles from './page.module.css';
import { useYokaiList } from '@/hooks/useYokai';
import { useUserTeams, useTeamMutations, useLocalTeam } from '@/hooks/useTeams';
import { useAttitudes, useEquipment } from '@/hooks/useGameData';
import { useUserStore } from '@/store/userStore';
import { useAudioStore } from '@/store/audioStore';
import { useTeamStore } from '@/store/teamStore';
import type { Yokai, TeamYokai, Team } from '@/lib/api/types';
import {
  createDefaultTeamYokai,
  getYokaiImageUrl,
} from '@/lib/teambuilder/utils';

export default function Teambuilder() {
  const router = useRouter();
  const { user } = useUserStore();
  const { isMuted } = useAudioStore();
  const { currentTeam, setCurrentTeam } = useTeamStore();

  // Data fetching
  const { yokaiList, loading: yokaiLoading } = useYokaiList();
  const { attitudesMap, loading: attitudesLoading } = useAttitudes();
  const { equipmentMap, loading: equipmentLoading } = useEquipment();
  
  // Use backend teams if logged in, otherwise use localStorage
  const { teams: backendTeams, loading: teamsLoading, refreshTeams } = useUserTeams(user?.id);
  const { createTeam: createBackendTeam, updateTeam: updateBackendTeam, deleteTeam: deleteBackendTeam, saving } = useTeamMutations(user?.id);

  // Local state
  const [localTeams, setLocalTeams] = useState<Team[]>([]);
  const [selectedTeamIndex, setSelectedTeamIndex] = useState(0);
  const [selectedPosition, setSelectedPosition] = useState<number | null>(null);
  const [teamYokaiList, setTeamYokaiList] = useState<(TeamYokai & { yokai?: Yokai })[]>([]);
  const [teamName, setTeamName] = useState('Untitled Team');
  const [teamType, setTeamType] = useState<'bony' | 'fleshy'>('bony');
  const [searchTerm, setSearchTerm] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [showYokaiList, setShowYokaiList] = useState(true);
  const [showItemList, setShowItemList] = useState(false);

  // Load teams from localStorage on mount (for non-logged-in users)
  useEffect(() => {
    if (!user) {
      const savedTeams = localStorage.getItem('teams');
      if (savedTeams) {
        try {
          const parsed = JSON.parse(savedTeams);
          setLocalTeams(parsed);
        } catch (err) {
          console.error('Failed to parse saved teams:', err);
          // Initialize with default team
          const defaultTeams: Team[] = [{
            id: 'local-1',
            name: 'Untitled Team',
            team_type: 'bony',
            yokai: [],
            user_id: 'local',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          }];
          setLocalTeams(defaultTeams);
          localStorage.setItem('teams', JSON.stringify(defaultTeams));
        }
      } else {
        // Initialize with default team
        const defaultTeams: Team[] = [{
          id: 'local-1',
          name: 'Untitled Team',
          team_type: 'bony',
          yokai: [],
          user_id: 'local',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        }];
        setLocalTeams(defaultTeams);
        localStorage.setItem('teams', JSON.stringify(defaultTeams));
      }
    }
  }, [user]);

  // Save local teams to localStorage whenever they change
  useEffect(() => {
    if (!user && localTeams.length > 0) {
      localStorage.setItem('teams', JSON.stringify(localTeams));
    }
  }, [localTeams, user]);

  // Determine which teams to use
  const teams = user ? backendTeams : localTeams;

  // Debounce search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchTerm);
    }, 300);
    return () => clearTimeout(timer);
  }, [searchTerm]);

  // Filtered and sorted Yo-kai list
  const filteredYokai = useMemo(() => {
    const term = debouncedSearch.toLowerCase().trim();
    let filtered = yokaiList;
    if (term) {
      filtered = yokaiList.filter(yokai =>
        yokai.name.toLowerCase().includes(term) ||
        yokai.tribe.toLowerCase().includes(term) ||
        yokai.rank.toLowerCase().includes(term)
      );
    }
    return filtered.slice(0, 50);
  }, [yokaiList, debouncedSearch]);

  // Load team when selection changes
  const yokaiListRef = useRef(yokaiList);
  useEffect(() => {
    yokaiListRef.current = yokaiList;
  }, [yokaiList]);

  useEffect(() => {
    if (teams.length > 0 && selectedTeamIndex < teams.length && yokaiListRef.current.length > 0) {
      const team = teams[selectedTeamIndex];
      setTeamName(team.name);
      setTeamType(team.team_type);
      
      // Convert team yokai to local format
      const yokaiWithData = team.yokai.map(ty => {
        const yokai = yokaiListRef.current.find(y => y.id === ty.yokai_id);
        return { ...ty, yokai };
      });
      setTeamYokaiList(yokaiWithData);
      setCurrentTeam(team);
    }
  }, [selectedTeamIndex, teams.length, setCurrentTeam]);

  // Get selected Yo-kai
  const selectedYokai = useMemo(() => {
    if (selectedPosition === null) return null;
    const teamYokai = teamYokaiList.find(ty => ty.position === selectedPosition);
    return teamYokai;
  }, [selectedPosition, teamYokaiList]);

  const handleSelectPosition = useCallback((position: number) => {
    setSelectedPosition(position);
    const teamYokai = teamYokaiList.find(ty => ty.position === position);
    if (teamYokai) {
      // Play select sound
    }
  }, [teamYokaiList]);

  const handleAddYokai = useCallback((yokai: Yokai) => {
    // Find first empty position or use position 0-5
    const usedPositions = new Set(teamYokaiList.map(ty => ty.position));
    let position = 0;
    while (usedPositions.has(position) && position < 6) {
      position++;
    }

    if (position >= 6) {
      alert('Team is full! Remove a Yo-kai first.');
      return;
    }

    const newTeamYokai = {
      ...createDefaultTeamYokai(yokai, position),
      yokai,
    };

    setTeamYokaiList([...teamYokaiList, newTeamYokai]);
    setSelectedPosition(position);
    
    // Play add sound
  }, [teamYokaiList]);

  const handleRemoveYokai = useCallback(() => {
    if (selectedPosition === null) return;
    
    setTeamYokaiList(teamYokaiList.filter(ty => ty.position !== selectedPosition));
    setSelectedPosition(null);
    
    // Play remove sound
  }, [selectedPosition, teamYokaiList]);

  const handleMoveYokai = useCallback((newPosition: number) => {
    if (selectedPosition === null) return;
    
    const updated = teamYokaiList.map(ty => {
      if (ty.position === selectedPosition) {
        return { ...ty, position: newPosition };
      }
      if (ty.position === newPosition) {
        return { ...ty, position: selectedPosition };
      }
      return ty;
    });
    
    setTeamYokaiList(updated);
    setSelectedPosition(newPosition);
  }, [selectedPosition, teamYokaiList]);

  const handleUpdateStat = useCallback((
    stat: 'hp' | 'str' | 'spr' | 'def' | 'spd',
    type: 'iv' | 'ev' | 'gym',
    value: number
  ) => {
    if (selectedPosition === null) return;

    const clampedValue = Math.max(0, Math.floor(value));
    let validated = clampedValue;
    
    if (type === 'iv') {
      validated = Math.min(clampedValue, 15);
    } else if (type === 'ev') {
      validated = Math.min(clampedValue, 252);
    } else if (type === 'gym') {
      validated = Math.min(clampedValue, 100);
    }
    
    setTeamYokaiList(teamYokaiList.map(ty => {
      if (ty.position !== selectedPosition) return ty;
      
      const updated = { ...ty };
      if (type === 'iv') {
        updated.ivs = { ...updated.ivs, [stat]: validated };
      } else if (type === 'ev') {
        const newEvs = { ...updated.evs, [stat]: validated };
        const total = newEvs.hp + newEvs.str + newEvs.spr + newEvs.def + newEvs.spd;
        if (total > 510) {
          alert('Total EVs cannot exceed 510!');
          return ty;
        }
        updated.evs = newEvs;
      } else if (type === 'gym' && stat !== 'hp') {
        updated.gym_points = { ...updated.gym_points, [stat]: validated };
      }
      
      return updated;
    }));
  }, [selectedPosition, teamYokaiList]);

  const handleSaveTeam = useCallback(async () => {
    const teamData = {
      name: teamName,
      team_type: teamType,
      yokai: teamYokaiList.map(({ yokai, ...ty }) => ty),
    };

    try {
      if (user) {
        // Save to backend
        if (currentTeam?.id) {
          await updateBackendTeam(currentTeam.id, teamData);
        } else {
          await createBackendTeam(teamData);
        }
        await refreshTeams();
        alert('Team saved successfully!');
      } else {
        // Save to localStorage
        const updatedTeams = [...localTeams];
        if (selectedTeamIndex < updatedTeams.length) {
          updatedTeams[selectedTeamIndex] = {
            ...updatedTeams[selectedTeamIndex],
            name: teamName,
            team_type: teamType,
            yokai: teamYokaiList.map(({ yokai, ...ty }) => ty),
            updated_at: new Date().toISOString(),
          };
        }
        setLocalTeams(updatedTeams);
        alert('Team saved to browser storage!');
      }
    } catch (error) {
      console.error('Failed to save team:', error);
      alert('Failed to save team');
    }
  }, [user, teamName, teamType, teamYokaiList, currentTeam, updateBackendTeam, createBackendTeam, refreshTeams, localTeams, selectedTeamIndex]);

  const handleDeleteTeam = useCallback(async () => {
    if (teams.length === 0) return;
    
    if (!confirm('Are you sure you want to delete this team?')) return;

    try {
      if (user && currentTeam?.id) {
        // Delete from backend
        await deleteBackendTeam(currentTeam.id);
        await refreshTeams();
      } else {
        // Delete from localStorage
        const updatedTeams = localTeams.filter((_, index) => index !== selectedTeamIndex);
        if (updatedTeams.length === 0) {
          // Ensure at least one team exists
          updatedTeams.push({
            id: `local-${Date.now()}`,
            name: 'Untitled Team',
            team_type: 'bony',
            yokai: [],
            user_id: 'local',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
          });
        }
        setLocalTeams(updatedTeams);
      }
      setSelectedTeamIndex(0);
      setTeamYokaiList([]);
      setSelectedPosition(null);
    } catch (error) {
      console.error('Failed to delete team:', error);
      alert('Failed to delete team');
    }
  }, [user, currentTeam, teams.length, deleteBackendTeam, refreshTeams, localTeams, selectedTeamIndex]);

  const handleCreateNewTeam = useCallback(async () => {
    const newTeamData = {
      name: 'New Team',
      team_type: 'bony' as const,
      yokai: [],
    };

    try {
      if (user) {
        // Create in backend
        await createBackendTeam(newTeamData);
        await refreshTeams();
        setSelectedTeamIndex(teams.length); // Select the new team
      } else {
        // Create in localStorage
        const newTeam: Team = {
          id: `local-${Date.now()}`,
          name: 'New Team',
          team_type: 'bony',
          yokai: [],
          user_id: 'local',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        };
        setLocalTeams([...localTeams, newTeam]);
        setSelectedTeamIndex(localTeams.length); // Select the new team
      }
    } catch (error) {
      console.error('Failed to create team:', error);
      alert('Failed to create team');
    }
  }, [user, createBackendTeam, refreshTeams, teams.length, localTeams]);

  // Debug logging
  useEffect(() => {
    console.log('[Teambuilder] Loading states:', {
      yokaiLoading,
      attitudesLoading,
      equipmentLoading,
      teamsLoading,
      user: !!user,
      yokaiCount: yokaiList.length,
      attitudesCount: Object.keys(attitudesMap).length,
      equipmentCount: Object.keys(equipmentMap).length,
      backendTeamsCount: backendTeams.length,
      localTeamsCount: localTeams.length,
    });
  }, [yokaiLoading, attitudesLoading, equipmentLoading, teamsLoading, user, yokaiList.length, attitudesMap, equipmentMap, backendTeams.length, localTeams.length]);

  // Only check backend teams loading if user is logged in
  const isLoading = yokaiLoading || attitudesLoading || equipmentLoading || (user ? teamsLoading : false);

  if (isLoading) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <p>Loading Teambuilder...</p>
          <p style={{ fontSize: '0.8em', marginTop: '10px' }}>
            {yokaiLoading && 'Loading Yo-kai...'}<br />
            {attitudesLoading && 'Loading attitudes...'}<br />
            {equipmentLoading && 'Loading equipment...'}<br />
            {user && teamsLoading && 'Loading teams...'}
          </p>
          <p style={{ fontSize: '0.7em', marginTop: '20px', color: '#999' }}>
            If this takes too long, make sure the backend is running:<br />
            <code>./start_backend.sh</code>
          </p>
        </div>
      </div>
    );
  }

  // If any critical data failed to load, show error with option to continue
  if (yokaiList.length === 0) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>
          <p style={{ color: '#ff6b6b', marginBottom: '20px' }}>
            ⚠️ Failed to load Yo-kai data from backend
          </p>
          <p style={{ fontSize: '0.9em', marginBottom: '20px' }}>
            The backend server at <code>localhost:8000</code> is not responding.
          </p>
          <p style={{ fontSize: '0.85em', marginBottom: '30px' }}>
            Start the backend with: <code>./start_backend.sh</code>
          </p>
          <button 
            onClick={() => window.location.reload()} 
            style={{ 
              padding: '10px 20px', 
              marginRight: '10px',
              cursor: 'pointer',
              background: '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
            }}
          >
            Retry
          </button>
          <button 
            onClick={() => router.push('/')}
            style={{ 
              padding: '10px 20px',
              cursor: 'pointer',
              background: '#666',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
            }}
          >
            Go Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      {/* Background */}
      <Image
        src="/images/teambuilder/padBGNew.png"
        alt="Background"
        fill
        className={styles.bg}
        priority
        sizes="100vw"
        unoptimized
      />

      {/* Home Button */}
      <button 
        className={styles.homeButton}
        onClick={() => router.push('/')}
      >
        <Image
          src="/images/teambuilder/padIcon.png"
          alt="Home"
          width={50}
          height={50}
        />
      </button>

      {/* Music Toggle */}
      <button className={styles.toggleMusic}>
        <Image
          src={isMuted ? "/images/musicOFF.png" : "/images/musicON.png"}
          alt="Toggle Music"
          width={50}
          height={50}
        />
      </button>

      {/* Yokai Display */}
      {selectedYokai?.yokai ? (
        <Image
          src={getYokaiImageUrl(selectedYokai.yokai, 'sprite')}
          alt={selectedYokai.yokai.name}
          width={300}
          height={400}
          className={styles.yokaiGif}
        />
      ) : (
        <Image
          src="/images/teambuilder/whisperPlaceholder.webp"
          alt="Yokai"
          width={300}
          height={400}
          className={styles.yokaiGif}
        />
      )}

      <p className={styles.yokaiName}>
        {selectedYokai?.yokai?.name || 'Select a Yo-kai!'}
      </p>

      {/* Yokai List */}
      <div className={`${styles.yokaiList} ${styles.uiBG}`}>
        <input
          type="text"
          placeholder="Search Yo-kai..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className={styles.searchInput}
        />
        
        <div className={styles.yokaiListScroll}>
          {filteredYokai.map(yokai => (
            <button
              key={yokai.id}
              onClick={() => handleAddYokai(yokai)}
              className={styles.yokaiOption}
            >
              <Image
                src={yokai.artwork_image || '/images/teambuilder/whisperPlaceholder.webp'}
                alt={yokai.name}
                width={40}
                height={40}
                className={styles.medalList}
                loading="lazy"
                unoptimized
              />
              <span>{yokai.name} | Rank: {yokai.rank}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Yokai Wheel */}
      <Image
        src="/images/teambuilder/yokaiWheel.webp"
        alt="Yokai Wheel"
        width={400}
        height={400}
        className={styles.yokaiWheel}
      />

      {/* Team Slots */}
      {[0, 1, 2, 3, 4, 5].map(position => {
        const teamYokai = teamYokaiList.find(ty => ty.position === position);
        return (
          <button
            key={position}
            className={styles[`slot${position + 1}`]}
            onClick={() => handleSelectPosition(position)}
            style={{
              border: selectedPosition === position ? '3px solid #ffd700' : 'none'
            }}
          >
            {teamYokai?.yokai ? (
              <Image
                src={getYokaiImageUrl(teamYokai.yokai, 'medal')}
                alt={teamYokai.yokai.name}
                width={60}
                height={60}
              />
            ) : (
              <div style={{ width: 60, height: 60 }} />
            )}
          </button>
        );
      })}

      {/* Yokai Management Buttons */}
      <button 
        className={styles.deleteYokai}
        onClick={handleRemoveYokai}
        disabled={selectedPosition === null}
      >
        Remove Selected Yokai
      </button>
      <button 
        className={styles.moveYokai}
        disabled={selectedPosition === null}
      >
        Move Selected Yokai
      </button>

      {/* Item List (Hidden for now) */}
      <div 
        className={`${styles.itemList} ${styles.uiBG}`}
        style={{ display: showItemList ? 'block' : 'none' }}
      >
        {equipmentLoading ? (
          <p>Loading equipment...</p>
        ) : (
          <div>
            {Object.values(equipmentMap).map(item => (
              <div key={item.id} className={styles.equipmentItem}>
                <span>{item.name}</span>
                <p>{item.description}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {selectedYokai && selectedYokai.yokai && (
        <div className={`${styles.currentInfo} ${styles.uiBG}`}>
          <p className={styles.currentText}>⸻IVs⸻EVs⸻Gym⸻</p>
          <br />
          
          <p className={styles.hpDisplay}>HP</p>
          <input
            type="number"
            className={styles.ivHP}
            value={selectedYokai.ivs.hp}
            onChange={(e) => handleUpdateStat('hp', 'iv', parseInt(e.target.value) || 0)}
            min={0}
            max={15}
          />
          <input
            type="number"
            className={styles.evHP}
            value={selectedYokai.evs.hp}
            onChange={(e) => handleUpdateStat('hp', 'ev', parseInt(e.target.value) || 0)}
            min={0}
            max={252}
          />
          <br />
          
          <p className={styles.strDisplay}>STR</p>
          <input
            type="number"
            className={styles.ivSTR}
            value={selectedYokai.ivs.str}
            onChange={(e) => handleUpdateStat('str', 'iv', parseInt(e.target.value) || 0)}
            min={0}
            max={15}
          />
          <input
            type="number"
            className={styles.evSTR}
            value={selectedYokai.evs.str}
            onChange={(e) => handleUpdateStat('str', 'ev', parseInt(e.target.value) || 0)}
            min={0}
            max={252}
          />
          <input
            type="number"
            className={styles.gpSTR}
            value={selectedYokai.gym_points.str}
            onChange={(e) => handleUpdateStat('str', 'gym', parseInt(e.target.value) || 0)}
            min={0}
            max={100}
          />
          <br />
          
          <p className={styles.sprDisplay}>SPR</p>
          <input
            type="number"
            className={styles.ivSPR}
            value={selectedYokai.ivs.spr}
            onChange={(e) => handleUpdateStat('spr', 'iv', parseInt(e.target.value) || 0)}
            min={0}
            max={15}
          />
          <input
            type="number"
            className={styles.evSPR}
            value={selectedYokai.evs.spr}
            onChange={(e) => handleUpdateStat('spr', 'ev', parseInt(e.target.value) || 0)}
            min={0}
            max={252}
          />
          <input
            type="number"
            className={styles.gpSPR}
            value={selectedYokai.gym_points.spr}
            onChange={(e) => handleUpdateStat('spr', 'gym', parseInt(e.target.value) || 0)}
            min={0}
            max={100}
          />
          <br />
          
          <p className={styles.defDisplay}>DEF</p>
          <input
            type="number"
            className={styles.ivDEF}
            value={selectedYokai.ivs.def}
            onChange={(e) => handleUpdateStat('def', 'iv', parseInt(e.target.value) || 0)}
            min={0}
            max={15}
          />
          <input
            type="number"
            className={styles.evDEF}
            value={selectedYokai.evs.def}
            onChange={(e) => handleUpdateStat('def', 'ev', parseInt(e.target.value) || 0)}
            min={0}
            max={252}
          />
          <input
            type="number"
            className={styles.gpDEF}
            value={selectedYokai.gym_points.def}
            onChange={(e) => handleUpdateStat('def', 'gym', parseInt(e.target.value) || 0)}
            min={0}
            max={100}
          />
          <br />
          
          <p className={styles.spdDisplay}>SPD</p>
          <input
            type="number"
            className={styles.ivSPD}
            value={selectedYokai.ivs.spd}
            onChange={(e) => handleUpdateStat('spd', 'iv', parseInt(e.target.value) || 0)}
            min={0}
            max={15}
          />
          <input
            type="number"
            className={styles.evSPD}
            value={selectedYokai.evs.spd}
            onChange={(e) => handleUpdateStat('spd', 'ev', parseInt(e.target.value) || 0)}
            min={0}
            max={252}
          />
          <input
            type="number"
            className={styles.gpSPD}
            value={selectedYokai.gym_points.spd}
            onChange={(e) => handleUpdateStat('spd', 'gym', parseInt(e.target.value) || 0)}
            min={0}
            max={100}
          />
          <br />
          
          {/* Attitude Selection */}
          <p className={styles.attitudeLabel}>Attitude:</p>
          <select
            className={styles.attitudeSelect}
            value={selectedYokai.attitude_id}
            onChange={(e) => {
              setTeamYokaiList(teamYokaiList.map(ty =>
                ty.position === selectedPosition
                  ? { ...ty, attitude_id: e.target.value }
                  : ty
              ));
            }}
          >
            {Object.values(attitudesMap).map(att => (
              <option key={att.id} value={att.id}>
                {att.name}
              </option>
            ))}
          </select>
        </div>
      )}

      {/* Stats Chart (Hidden for now) */}
      <div className={styles.statsChart} style={{ display: 'none' }}></div>

      {/* Prob Chart (Hidden for now) */}
      <div className={styles.probChart} style={{ display: 'none' }}></div>

      {/* AP Display (Hidden for now) */}
      <div className={styles.apDisplay} style={{ display: 'none' }}></div>

      {/* Team Type Buttons */}
      <button
        className={styles.setBony}
        onClick={() => setTeamType('bony')}
        style={{
          display: 'block',
          backgroundColor: teamType === 'bony' ? '#ff6b6b' : '#ccc'
        }}
      >
        Bony
      </button>
      <button
        className={styles.setFleshy}
        onClick={() => setTeamType('fleshy')}
        style={{
          display: 'block',
          backgroundColor: teamType === 'fleshy' ? '#4ecdc4' : '#ccc'
        }}
      >
        Fleshy
      </button>

      {/* Team Management Section */}
      <div className={styles.teamManagement}>
        <select
          className={styles.teamSelect}
          value={selectedTeamIndex}
          onChange={(e) => setSelectedTeamIndex(parseInt(e.target.value))}
        >
          {teams.map((team, index) => (
            <option key={team.id} value={index}>
              {team.name}
            </option>
          ))}
        </select>

        <input
          type="text"
          className={styles.nameTeam}
          value={teamName}
          onChange={(e) => setTeamName(e.target.value)}
          placeholder="Team Name"
        />

        <button
          className={styles.createTeam}
          onClick={handleCreateNewTeam}
          disabled={saving}
        >
          New Team
        </button>

        <button
          className={styles.saveTeam}
          onClick={handleSaveTeam}
          disabled={saving}
        >
          {saving ? 'Saving...' : 'Save Team'}
        </button>

        <button
          className={styles.renameTeam}
          onClick={handleSaveTeam}
          disabled={saving}
        >
          Rename
        </button>

        <button
          className={styles.deleteTeam}
          onClick={handleDeleteTeam}
          disabled={!currentTeam?.id}
        >
          Delete Team
        </button>
      </div>

      {/* Paste Output (Hidden for now) */}
      <div className={styles.pasteOutput} style={{ display: 'none' }}></div>

      {/* Transition Pad */}
      <Image
        src="/images/padTrans.png"
        alt="Transition"
        fill
        className={styles.padTrans}
        sizes="100vw"
        unoptimized
        style={{ display: 'none' }}
      />
    </div>
  );
}
