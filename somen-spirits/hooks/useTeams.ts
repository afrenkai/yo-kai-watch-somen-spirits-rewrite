'use client';

import { useEffect, useState, useCallback } from 'react';
import { teamsApi } from '@/lib/api';
import type { Team, TeamYokai } from '@/lib/api/types';

export function useTeam(id?: string) {
  const [team, setTeam] = useState<Team | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    if (!id) {
      setLoading(false);
      return;
    }

    let cancelled = false;

    async function fetchTeam(teamId: string) {
      try {
        setLoading(true);
        setError(null);
        const data = await teamsApi.getById(teamId);
        if (!cancelled) {
          setTeam(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err : new Error('Failed to fetch team'));
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchTeam(id);

    return () => {
      cancelled = true;
    };
  }, [id]);

  return { team, loading, error };
}

export function useUserTeams(userId?: string) {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const refreshTeams = useCallback(async () => {
    if (!userId) {
      setLoading(false);
      setTeams([]);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await teamsApi.getByUserId(userId);
      setTeams(data);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch teams'));
    } finally {
      setLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    refreshTeams();
  }, [refreshTeams]);

  return { teams, loading, error, refreshTeams };
}

export function useTeamMutations(userId?: string) {
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const createTeam = useCallback(async (teamData: {
    name: string;
    team_type: 'bony' | 'fleshy';
    yokai: TeamYokai[];
  }) => {
    if (!userId) {
      throw new Error('User ID required to create team');
    }

    try {
      setSaving(true);
      setError(null);
      const newTeam = await teamsApi.create({
        user_id: userId,
        ...teamData,
      });
      return newTeam;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to create team');
      setError(error);
      throw error;
    } finally {
      setSaving(false);
    }
  }, [userId]);

  const updateTeam = useCallback(async (id: string, teamData: {
    name?: string;
    team_type?: 'bony' | 'fleshy';
    yokai?: TeamYokai[];
  }) => {
    try {
      setSaving(true);
      setError(null);
      const updatedTeam = await teamsApi.update(id, teamData);
      return updatedTeam;
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to update team');
      setError(error);
      throw error;
    } finally {
      setSaving(false);
    }
  }, []);

  const deleteTeam = useCallback(async (id: string) => {
    try {
      setSaving(true);
      setError(null);
      await teamsApi.delete(id);
    } catch (err) {
      const error = err instanceof Error ? err : new Error('Failed to delete team');
      setError(error);
      throw error;
    } finally {
      setSaving(false);
    }
  }, []);

  return {
    createTeam,
    updateTeam,
    deleteTeam,
    saving,
    error,
  };
}

/**
 * Hook for managing team in localStorage for offline editing
 */
export function useLocalTeam(teamId: string) {
  const [localTeam, setLocalTeam] = useState<Team | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem(`team_${teamId}`);
    if (saved) {
      try {
        setLocalTeam(JSON.parse(saved));
      } catch (err) {
        console.error('Failed to parse saved team:', err);
      }
    }
  }, [teamId]);

  const saveLocal = useCallback((team: Team) => {
    localStorage.setItem(`team_${teamId}`, JSON.stringify(team));
    setLocalTeam(team);
  }, [teamId]);

  const clearLocal = useCallback(() => {
    localStorage.removeItem(`team_${teamId}`);
    setLocalTeam(null);
  }, [teamId]);

  return {
    localTeam,
    saveLocal,
    clearLocal,
  };
}
